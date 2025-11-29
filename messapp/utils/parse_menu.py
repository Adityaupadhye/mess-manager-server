import pandas as pd
import json
from datetime import datetime

MEAL_MAP = {
    "BREAKFAST": "breakfast",
    "LUNCH": "lunch",
    "TIFFIN": "snacks",
    "DINNER": "dinner",
    "MILK": "milk",
}

def parse_menu_csv(csv_path):
    df = pd.read_csv(csv_path, header=None)

    # === 1. Extract date row (2..8 columns) ===
    raw_dates = df.iloc[1, 2:9].tolist()
    dates = [
        datetime.strptime(d, "%d-%b-%Y").strftime("%Y-%m-%d")
        for d in raw_dates
        if isinstance(d, str)
    ]

    result = []
    current_meal = None

    # Loop through all rows after date row
    for r in range(2, df.shape[0]):
        meal_cell = str(df.iloc[r, 0]).strip() if pd.notna(df.iloc[r, 0]) else ""

        # Detect new meal section
        if meal_cell in MEAL_MAP:
            current_meal = MEAL_MAP[meal_cell]

        if current_meal is None:
            continue

        # Collect column-wise items (C–I)
        row_values = []
        non_empty_count = 0

        for c in range(2, 9):
            val = df.iloc[r, c]

            if pd.isna(val) or str(val).strip() == "":
                row_values.append(None)
                continue

            text = str(val).strip()
            non_empty_count += 1

            # DO NOT SKIP PEST CONTROL ANYMORE
            parts = [p.strip() for p in text.replace("\n", ",").split(",") if p.strip()]
            row_values.append(parts)

        # === Handle merged cell row ===
        # Example: [ "Pest Control", None, None, None, None, None, None ]
        if non_empty_count == 1:
            for day_index, parts in enumerate(row_values):
                if parts is not None:     # this is merged cell
                    result.append({
                        "date": dates[day_index],
                        "meal_type": current_meal,
                        "items": parts
                    })
            continue

        # === Normal row (multiple day-wise items) ===
        for day_index, parts in enumerate(row_values):
            if parts is None:
                continue

            result.append({
                "date": dates[day_index],
                "meal_type": current_meal,
                "items": parts
            })

    # === 3. Combine multiple rows for same date + meal ===
    combined = {}

    for entry in result:
        key = (entry["date"], entry["meal_type"])
        combined.setdefault(key, []).extend(entry["items"])

    # === 4. Remove duplicates ===
    final = []
    for (date, meal_type), items in combined.items():
        clean = []
        seen = set()

        for item in items:
            tup = tuple(item)
            if tup not in seen:
                seen.add(tup)
                clean.append(item)

        final.append({
            "date": date,
            "meal_type": meal_type,
            "items": clean
        })

    return final


if __name__ == "__main__":
    data = parse_menu_csv("menu.csv")
    print(json.dumps(data, indent=4, default=str))
