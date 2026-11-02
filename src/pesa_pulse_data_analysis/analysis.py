import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Could nt fetch data:{error}")
        return []

def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key,value in record.items():
        print(f"{' '* indent}{key}: {type(value).__name__}")

        if isinstance(value, dict):
            explore(value, indent + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    explore(item, indent + 1)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []

    for customer in customers:
        address = customer["address"]
        geo = address["geo"]
        email = customer["email"]
        email_domain = email.rsplit(".", 1)[-1]

        row = {
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": email,
            "email_domain": email_domain,
            "phone": customer["phone"],
            "city": address["city"],
            "zipcode": address["zipcode"],
            "latitude": float(geo["lat"]),
            "longitude": float(geo["lng"]),
            "company": customer["company"]["name"],
            "website": customer["website"],
        }
        rows.append(row)

    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]
        counts[city] = counts.get(city, 0) + 1

    return counts





def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = [customer["email"].rsplit("@", 1)[1].rsplit(".", 1)[-1]
               for customer in customers]
    return {domain: domains.count(domain) for domain in set(domains)}


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Covert the data into a dataframe"""
    return pd.DataFrame(rows)

def plot_distribution(
    counts: dict[str, int],
    path: Path,
    title: str,
    x_label: str,
) -> None:
    """Save a labelled chart of a distribution to path."""
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="steelblue")
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


def main() -> None:
    customers = get_customers()

    # One check handles a failed request or an empty response.
    if not customers:
        print("No customer data available. Stopping analysis.")
        return

    print(f"Retrieved {len(customers)} customers")

    print("\nStructure of the first customer:")
    explore(customers[0])

    # Prepare the cleaned records and summaries once.
    rows = extract_attributes(customers)
    df = to_dataframe(rows)
    city_count_data = city_counts(customers)
    domain_count_data = email_domain_counts(customers)

    print("\nFirst flattened customer:")
    print(rows[0])

    cities = unique_cities(customers)
    print(f"\nUnique cities: {len(cities)}")
    print(f"Customers: {len(customers)}")

    if len(cities) == len(customers):
        print(
            "Marketing takeaway: Each customer in this sample is in a "
            "different city."
        )
    else:
        print(
            "Marketing takeaway: Some customers in this sample share a city."
        )

    # Sort by customer count (highest first), then city name alphabetically.
    sorted_city_counts = sorted(
        city_count_data.items(),
        key=lambda item: (-item[1], item[0]),
    )

    print("\nCustomers by city:")
    for city, count in sorted_city_counts:
        print(f"{city}: {count}")

    print("\nCustomers by email domain:")
    for domain, count in sorted(
        domain_count_data.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        print(f"{domain}: {count}")

    print("\nDataFrame shape:", df.shape)
    print("\nColumn data types:")
    print(df.dtypes)

    pandas_city_counts = df["city"].value_counts().to_dict()
    print("\nPandas city counts:")
    print(df["city"].value_counts().sort_values(ascending=False))
    print(
        "Pandas counts match the Python counts:",
        pandas_city_counts == city_count_data,
    )

    # The script is under src/pesa_pulse_data_analysis/,
    # so parents[2] points to the project root.
    output_dir = Path(__file__).resolve().parents[2] / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / "customers.csv", index=False)

    city_df = pd.DataFrame(
        sorted_city_counts,
        columns=["city", "customer_count"],
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    plot_distribution(
        city_count_data,
        output_dir / "customer_distribution.png",
        title="Customers by City",
        x_label="City",
    )

    plot_distribution(
        domain_count_data,
        output_dir / "email_domain_distribution.png",
        title="Customers by Email Top-Level Domain",
        x_label="Email Top-Level Domain",
    )

    print(f"\nSaved CSV files and charts to: {output_dir}")


if __name__ == "__main__":
    main()
