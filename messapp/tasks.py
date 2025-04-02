# tasks.py
from datetime import datetime
from django.utils.timezone import make_aware
from .models import FoodLog

def process_foodlogs_sync(foodlogs_data):
    new_logs = []
    duplicate_logs = 0

    for entry in foodlogs_data:
        roll_no = entry.get('roll_no')
        food_category = entry.get('food_category')
        unix_timestamp = entry.get('timestamp')
        type = entry.get('type')

        try:
            timestamp = make_aware(datetime.fromtimestamp(unix_timestamp))
            log_date = timestamp.date()

            # Check if a record with the same roll_no, food_category, and date exists
            if FoodLog.objects.filter(roll_no=roll_no, food_category=food_category, date=log_date).exists():
                duplicate_logs += 1
                continue

            # Create FoodLog instance
            food_log = FoodLog(
                roll_no=roll_no,
                food_category=food_category,
                timestamp=timestamp,
                type=type,
                date=log_date,
                time=timestamp.time()
            )
            new_logs.append(food_log)
        except Exception as e:
            # Optionally log error details
            print(f"Error processing entry: {e}")
            continue

    if new_logs:
        FoodLog.objects.bulk_create(new_logs)

    # Log summary (or write to a log file)
    print(f"Background process complete: {len(new_logs)} new logs, {duplicate_logs} duplicates")
    return {"new_logs_count": len(new_logs), "duplicate_logs_count": duplicate_logs}
