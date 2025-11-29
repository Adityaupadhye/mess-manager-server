import pandas as pd
import json
import csv

data = []
def parse_students(csv_path):
    df = pd.read_csv(csv_path, header=None)

    # Read CSV file
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "Name": row["Name"],
                "Roll Number": row["Roll Number"],
                "Hostel": row["Hostel"]
            })
            # Now `data` is a list of dictionaries (JSON-like array)

        return data

# --------------------------
# Run & Print Output
# --------------------------
if __name__ == "__main__":
    data = parse_students("students.csv")
    json_array = json.dumps(data, indent=4)  # Convert to JSON string if needed
    print(json_array)
