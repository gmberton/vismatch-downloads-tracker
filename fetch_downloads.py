#!/usr/bin/env python3
"""
Fetch download counts for all models in the vismatch HuggingFace organization.
Appends data to downloads.csv with the current date.
"""

import os
import csv
from datetime import datetime
from huggingface_hub import HfApi
import sys

def fetch_download_counts():
    """Fetch download counts for all models in vismatch org."""
    api = HfApi()

    print("Fetching models from vismatch organization...")
    try:
        models = list(api.list_models(author="vismatch"))
    except Exception as e:
        print(f"Error fetching models: {e}")
        sys.exit(1)

    if not models:
        print("No models found in vismatch organization")
        sys.exit(1)

    # Extract model names and download counts
    model_data = {}
    for model in models:
        model_name = model.id.replace("vismatch/", "")
        downloads = model.downloads if hasattr(model, 'downloads') else 0
        model_data[model_name] = downloads
        print(f"  {model_name}: {downloads:,} downloads")

    return model_data

def update_csv(model_data):
    """Update the CSV file with today's download counts."""
    csv_file = "downloads.csv"
    today = datetime.now().strftime("%Y-%m-%d")

    # Check if CSV exists and read existing headers
    file_exists = os.path.isfile(csv_file)
    existing_models = []

    if file_exists:
        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            existing_models = headers[1:]  # Skip 'date' column

    # Combine existing and new models (preserve order, add new ones at end)
    all_models = existing_models.copy()
    for model in sorted(model_data.keys()):
        if model not in all_models:
            all_models.append(model)

    # Prepare the new row
    new_row = [today] + [model_data.get(model, 0) for model in all_models]

    # Write to CSV
    if not file_exists:
        # Create new file with headers
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date'] + all_models)
            writer.writerow(new_row)
        print(f"\nCreated {csv_file} with {len(all_models)} models")
    else:
        # Append to existing file
        # If new models were added, we need to rewrite the file with updated headers
        if len(all_models) > len(existing_models):
            print(f"\nNew models detected: {set(all_models) - set(existing_models)}")
            # Read all existing data
            with open(csv_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                existing_data = list(reader)

            # Rewrite with new headers
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date'] + all_models)

                # Write old data with new columns (filled with 0 for missing values)
                for row in existing_data:
                    date = row['date']
                    values = [row.get(model, '0') for model in all_models]
                    writer.writerow([date] + values)

                # Write new row
                writer.writerow(new_row)
        else:
            # Just append the new row
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(new_row)

        print(f"\nUpdated {csv_file} with data for {today}")

    print(f"Total models tracked: {len(all_models)}")

def main():
    print(f"Starting download count fetch at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    model_data = fetch_download_counts()
    update_csv(model_data)

    print("=" * 60)
    print("Done!")

if __name__ == "__main__":
    main()
