import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import os

def fetch_snow_depth_data(year, month, day, city, county):
    city_formatted = city.replace(' ', '+')
    county_formatted = county.replace(' ', '+')
    url = f'https://www.nohrsc.noaa.gov/nearest/index.html?city={city_formatted}&county={county_formatted}&l=5&u=e&y={year}&m={month}&d={day}'
    print(f'Fetching data for {year}-{month:02d}-{day:02d} from {url}')
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Failed to retrieve data for {year}-{month:02d}-{day:02d}, status code: {response.status_code}')
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    target_table = None
    for table in tables:
        caption = table.find('caption')
        if caption and 'Snow Depth Observations' in caption.get_text():
            target_table = table
            break
    
    if not target_table:
        print(f'No "Snow Depth Observations" table found for {year}-{month:02d}-{day:02d}')
        return []
    
    rows = target_table.find_all('tr')[1:]  # Skip header row
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 5:
            print(f'Unexpected row format in year {year}: {row}')
            continue
        station_id = cols[0].text.strip()
        name = cols[1].text.strip()
        elevation = cols[2].text.strip().replace(',', '')
        elevation = int(elevation) if elevation.isdigit() else None
        snow_depth = cols[3].text.strip()
        snow_depth = float(snow_depth) if snow_depth.replace('.', '', 1).isdigit() else None
        date_str = cols[4].text.strip()
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d %H')
        except ValueError:
            print(f'Invalid date format in year {year}: {date_str}')
            date = None
        data.append([station_id, name, elevation, snow_depth, date, year])
    return data

def plot_station_data(df, output_dir):
    stations = df['Station ID'].unique()
    for station in stations:
        station_data = df[df['Station ID'] == station]
        plt.figure(figsize=(10, 6))
        plt.plot(station_data['Date'], station_data['Snow Depth (in)'], marker='o', linestyle='-')
        plt.title(f"Snow Depth Over Time for Station {station}")
        plt.xlabel("Date")
        plt.ylabel("Snow Depth (inches)")
        plt.grid(True)
        plt.tight_layout()
        # Save the plot as a PNG file in the output directory
        plot_filename = os.path.join(output_dir, f"station_{station}.png")
        plt.savefig(plot_filename)
        plt.close()
        print(f"Plot saved for station {station} at {plot_filename}")

def main():
    parser = argparse.ArgumentParser(description='Fetch and plot snow depth data for a specific city and county.')
    parser.add_argument('--city', type=str, default='Escalante', help='Name of the city (default: Escalante)')
    parser.add_argument('--county', type=str, default='Garfield', help='Name of the county (default: Garfield)')
    parser.add_argument('--years', type=int, default=6, help='Number of past years to retrieve data for, including the current year (default: 6)')
    parser.add_argument('--month', type=int, default=2, choices=range(1, 13), help='Month for data retrieval (1-12, default: 2)')
    parser.add_argument('--day', type=int, default=28, choices=range(1, 32), help='Day for data retrieval (1-31, default: 28)')
    parser.add_argument('--output', type=str, default='snow_depth_data.csv', help='Output CSV file name (default: snow_depth_data.csv)')
    parser.add_argument('--plot_dir', type=str, default='plots', help='Directory to save station plots (default: plots)')
    args = parser.parse_args()

    current_year = datetime.now().year
    start_year = current_year - args.years + 1
    years = range(start_year, current_year + 1)
    all_data = []
    for year in years:
        data = fetch_snow_depth_data(year, args.month, args.day, args.city, args.county)
        if data:
            all_data.extend(data)
        else:
            print(f'No data retrieved for {year}')
    
    if not all_data:
        print('No data retrieved for any year.')
        return
    
    df = pd.DataFrame(all_data, columns=['Station ID', 'Name', 'Elevation (ft)', 'Snow Depth (in)', 'Date', 'Year'])
    df.sort_values(by=['Station ID', 'Date'], inplace=True)
    
    # Save the DataFrame to a CSV file
    df.to_csv(args.output, index=False)
    print(f'Data successfully saved to {args.output}')

    # Create the plot directory if it doesn't exist
    os.makedirs(args.plot_dir, exist_ok=True)
    
    # Plot data for each station
    plot_station_data(df, args.plot_dir)

if __name__ == '__main__':
    main()
