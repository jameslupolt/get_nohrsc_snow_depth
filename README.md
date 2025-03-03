# Snow Depth Data Retrieval and Visualization Script

This script fetches snow depth data for a specified city and county on a given date over a specified number of years, saves the data to a CSV file, and generates plots for each station.

## Dependencies

Before running the script, ensure you have the following Python libraries installed:

- `requests`: For sending HTTP requests to retrieve web content.
- `beautifulsoup4`: For parsing HTML content.
- `pandas`: For data manipulation and analysis.
- `matplotlib`: For creating visualizations.

You can install these dependencies using `pip`. It's recommended to use a virtual environment to manage your Python packages. Here's how you can set it up:

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

2. **Install the required packages:**

   ```bash
   pip install requests beautifulsoup4 pandas matplotlib
   ```

Alternatively, you can create a `requirements.txt` file with the following content:

```
requests
beautifulsoup4
pandas
matplotlib
```

And install the dependencies using:

```bash
pip install -r requirements.txt
```

## Running the Script

The script accepts several command-line arguments to customize its behavior:

- `--city`: Name of the city (default: 'Escalante').
- `--county`: Name of the county (default: 'Garfield').
- `--years`: Number of past years to retrieve data for, including the current year (default: 6).
- `--month`: Month for data retrieval (1-12, default: 2).
- `--day`: Day for data retrieval (1-31, default: 28).
- `--output`: Output CSV file name (default: 'snow_depth_data.csv').
- `--plot_dir`: Directory to save station plots (default: 'plots').

**Syntax:**

```bash
python get_nohrsc_snow_depth.py --city CITY_NAME --county COUNTY_NAME --years NUMBER_OF_YEARS --month MONTH --day DAY --output OUTPUT_FILE --plot_dir PLOT_DIRECTORY
```

**Example:**

```bash
python get_nohrsc_snow_depth.py --city "Escalante" --county "Garfield" --years 6 --month 2 --day 28 --output "snow_depth_data.csv" --plot_dir "station_plots"
```

This command will:

- Fetch snow depth data for Escalante city in Garfield county on February 28 over the past 6 years.
- Save the consolidated data to 'snow_depth_data.csv'.
- Generate individual plots for each station and save them in the 'station_plots' directory.

**Note:** Ensure that the city and county names are correctly spelled and formatted to match the data available on the NOHRSC website.

## Additional Information

- The script uses Python's `argparse` module to handle command-line arguments.
- Plots are generated using `matplotlib` and saved in the specified directory.
- Data is fetched from the NOHRSC website based on the provided city and county names.

For more details on the libraries used:

- **Requests:** [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
- **BeautifulSoup:** [https://pypi.org/project/beautifulsoup4/](https://pypi.org/project/beautifulsoup4/)
- **Pandas:** [https://pandas.pydata.org/](https://pandas.pydata.org/)
- **Matplotlib:** [https://matplotlib.org/](https://matplotlib.org/)

Ensure you have a stable internet connection when running the script, as it fetches data from an online source.

By following the above instructions, you should be able to set up the environment, install necessary dependencies, and run the script to fetch and visualize snow depth data for your specified location.
```
