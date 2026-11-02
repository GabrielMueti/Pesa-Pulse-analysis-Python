# Pesa Pulse Customer Analysis

This project explores customer records retrieved from an API. It provides practice with Python requests, nested JSON data, sets, dictionaries, pandas, CSV exports, and data visualization.

> **About the data:** This project uses sample records from JSONPlaceholder. The findings describe its 10 example users, not Pesa Pulse’s or its partner’s real customer directory.

## What the analysis does

The script:

1. Retrieves customer records from the JSONPlaceholder Users API using Python’s `requests` library and a timeout. If the request fails, it prints a message and returns an empty list. The main function checks for missing data once and stops before continuing.
2. Recursively explores a customer record and prints each field’s name and Python type.
3. Extracts 12 fields into a flat record for each customer: `customer_id`, name, username, email, email top-level domain, phone, city, zipcode, latitude, longitude, company, and website. Latitude and longitude are converted to floats.
4. Uses a set to find distinct cities and a Python dictionary to count customers by city.
5. Counts email top-level domains using a dictionary comprehension.
6. Converts the flattened records into a pandas DataFrame and compares pandas’ city counts with the counts calculated in Python.
7. Saves the customer records and city counts as CSV files and creates charts for customers by city and by email top-level domain.

## Understanding the nested data

The API returns each customer as a dictionary. Some values are nested dictionaries:

- `address` contains the street, suite, city, zipcode, and `geo` fields.
- `address["geo"]` contains the latitude (`lat`) and longitude (`lng`).
- `company` contains the company name and other company details.

For example, the path to a customer’s latitude is:

```text
customer → address → geo → lat
```

The script extracts selected values from these nested dictionaries so that each customer can be represented as one flat row in the DataFrame and customer CSV.

## Findings from the sample

The API returned **10 customers**.

- The customers are in **10 distinct cities**, with one customer in each city. No city has a higher count in this sample.
- The most common email top-level domain is **`biz`**, appearing for 3 customers. Each of the other seven customers has a different top-level domain.
- The pandas DataFrame contains **10 rows and 12 columns**.
- The Python city counts and pandas `value_counts()` agree for this sample.

The city chart shows that this sample has one customer in each city, so it does not reveal a location with a higher concentration. The email top-level-domain chart shows more variation in this particular sample. Neither chart is enough to plan real regional campaigns; that requires the partner’s complete, current customer directory.

## Project structure

```text
Pesa-Pulse-analysis-Python/
├── src/
│   └── pesa_pulse_data_analysis/
│       └── analysis.py
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   ├── customer_distribution.png
│   └── email_domain_distribution.png
└── README.md
```

The script creates the top-level `output/` folder if it does not already exist.

## Requirements

- Python 3.11 or later
- `uv`

The project dependencies are recorded in `pyproject.toml` and `uv.lock`. `requirements.txt` is included for environments that install dependencies with `pip`.

## How to run the analysis

Open a terminal in the project root—the folder containing `pyproject.toml`—and run:

```powershell
uv sync
uv run python src/pesa_pulse_data_analysis/analysis.py
```

The script retrieves records from the [JSONPlaceholder Users API](https://jsonplaceholder.typicode.com/users), so an internet connection is needed.

After it runs, check the top-level `output/` folder for the two CSV files and two charts.

## Assumptions and limitations

- JSONPlaceholder is a mock API. Its 10 example users are not Pesa Pulse customers and may not reflect the partner’s directory.
- The `email_domain` field contains the part after the final dot in an email address. For example, `Sincere@april.biz` produces `biz`.
- The city chart summarizes only the records returned by the sample API. Since each city appears once, it does not identify a city with a larger customer concentration.
- The city-count CSV is sorted by customer count from highest to lowest, then by city name alphabetically for ties.
- Campaign planning should use the partner’s full, current customer directory.
