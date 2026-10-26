# Pesa Pulse Customer Analysis

This project retrieves customer records from the JSONPlaceholder API and explores them using Python. It shows how to work with API requests, nested JSON data, sets, dictionaries, pandas, CSV files, and charts.

> **Data note:** JSONPlaceholder returns sample data. The findings in this README describe its 10 example records, not Pesa Pulse’s actual customer directory.

## What the analysis does

The script follows the data from the API response through to the files it creates:

1. **Retrieves customer records** using Python’s `requests` library. The request has a timeout, checks for an unsuccessful HTTP response, and prints a clear message if the request fails.
2. **Explores the record structure** by walking through nested dictionaries and lists and printing each field’s name and Python type.
3. **Extracts customer details** into one flat dictionary per customer. The selected fields are ID, name, username, email, email top-level domain, phone, city, zipcode, latitude, longitude, company, and website. Latitude and longitude are converted to floats.
4. **Finds and counts locations** using a set to identify distinct cities and a dictionary to count customers in each city.
5. **Counts email top-level domains** with a dictionary comprehension. For example, `Sincere@april.biz` has the top-level domain `biz`.
6. **Checks the results with pandas** by converting the flattened records into a DataFrame and comparing its city counts with the counts calculated using Python dictionaries.
7. **Saves the results** as customer and city-count CSV files and creates a chart showing customers by city.

## Understanding the nested data

Each customer returned by the API is a dictionary. Some of its values are dictionaries too:

- `address` contains the street, suite, city, zipcode, and `geo` fields.
- `address["geo"]` contains the latitude (`lat`) and longitude (`lng`).
- `company` contains the company name and other company details.

For example, the path to a customer’s latitude is:

```text
customer → address → geo → lat
```

The script extracts selected values from those nested dictionaries so each customer can be represented as one flat row in the DataFrame and CSV file.

## Findings from the sample

The API returned **10 customers**.

- The customers are in **10 distinct cities**, with one customer in each city. There is no city with a higher customer count in this sample.
- The most common email top-level domain is **`biz`**, which appears for 3 customers. Each of the other seven customers has a different top-level domain.
- The pandas DataFrame contains **10 rows and 12 columns**.

The city chart shows that the sample has one customer per city, but it does not show a location with a larger concentration. The email top-level-domain counts have more variation in this sample. These findings are useful for practising the analysis, but they are not enough to plan real regional campaigns. That would require the partner’s complete, current customer directory.

## Project files

```text
Pesa-Pulse-Data-Analysis/
├── src/
│   └── pesa_pulse_data_analysis/
│       ├── analysis.py
│       └── output/
│           ├── customers.csv
│           ├── city_counts.csv
│           └── customer_distribution.png
├── pyproject.toml
├── uv.lock
├── requirements.txt
└── README.md
```

The script saves the CSV files and chart in `src/pesa_pulse_data_analysis/output/`.

## Requirements

- Python 3.11 or later
- `uv`

The project dependencies are recorded in `pyproject.toml` and `uv.lock`. The `requirements.txt` file is also included for tools that install dependencies with `pip`.

## How to run the analysis

Open a terminal in the project root—the folder containing `pyproject.toml`—and run:

```powershell
uv sync
uv run python src/pesa_pulse_data_analysis/analysis.py
```

The script retrieves records from the [JSONPlaceholder Users API](https://jsonplaceholder.typicode.com/users), so an internet connection is needed for the request to succeed.

After the script runs, check `src/pesa_pulse_data_analysis/output/` for the CSV files and chart.

## Assumptions and limitations

- JSONPlaceholder is a mock API. Its 10 example users are not Pesa Pulse customers and may not reflect the partner’s directory.
- The `email_domain` field contains the part after the final dot in an email address. For example, `Sincere@april.biz` gives `biz`.
- The city chart summarizes only the records returned by the sample API. Since every city appears once, it does not identify a city with a higher customer concentration.
- Campaign planning should use the partner’s full, current customer directory.
