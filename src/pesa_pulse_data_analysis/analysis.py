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
        return None

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
            "id": customer["id"],
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

def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    cities = list(counts.keys())
    customer_totals = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(cities, customer_totals, color="steelblue")
    plt.title("Customers by City")
    plt.xlabel("City")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    plt.close()


if __name__ == "__main__":
    # TODO: run each step and print a short findings summary
    customers = get_customers()

    ##Confirm customers are fetched
    if customers is not None:
        print(f"Retrieved {len(customers)} customers")
        print(customers[0])


    ##Explore nested dictionaries and lists
    if customers:
        print("\nStructure of the first customer:")
        explore(customers[0])


    ##Extract customer attributes
    if customers:
        rows = extract_attributes(customers)
        print("\nFirst flattened customer:")
        print(rows[1])

    ##Find unique cities using sets
    if customers:
        cities = unique_cities(customers)
        print(f"\nUnique cities: {len(cities)}")
        print(f"Customers: {len(customers)}")
        print(
            "Marketing takeaway: "
            "There are as many unique cities as customers, so each customer in this sample is in a different city. "

            if len(cities) == len(customers)
            else "Some customers share a city, so campaigns can target at least one location with multiple customers. "
        )
    ##Count customers by city
    print("\nCustomers by city:")
    for city, count in sorted(city_counts(customers).items(),
                              key=lambda item: item[1], reverse=True):
        print(f"{city}: {count}")

    ##Count customers by email domain
    print("\nCustomers by email domain:")
    for domain, count in sorted(email_domain_counts(customers).items(),
                                key=lambda item: item[1], reverse=True):
        print(f"{domain}: {count}")


    if customers:
       df = to_dataframe(rows)

       ##Dataframe details
       print("\nDataFrame shape:", df.shape)
       print("\nColumn data types:")
       print(df.dtypes)
       print("\nPandas customer counts by city:")
       print(df["city"].value_counts().sort_values(ascending=False))


    ##Export dataframe as CSV and save to path
    if customers:
        rows = extract_attributes(customers)
        df = to_dataframe(rows)

        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)

        df.to_csv(output_dir / "customers.csv", index=False)

        city_df = (
            df["city"]
            .value_counts()
            .rename_axis("city")
            .reset_index(name="customer_count")
        )
        city_df.to_csv(output_dir / "city_counts.csv", index=False)

        print(f"\nSaved customer and city CSV files to: {output_dir}")


    ##Visulaize the customer distribution and save to output folder
    city_counts_data = city_counts(customers)
    output_dir = Path(__file__).parent / "output"
    plot_distribution(
        city_counts_data,
        output_dir / "customer_distribution.png",
    )