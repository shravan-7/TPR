from django.db import IntegrityError
import csv
from Tourist_App.models import Dataset,DatasetLoaded

def import_csv_data():
    # Check if the dataset has already been loaded
    if DatasetLoaded.objects.filter(is_loaded=True).exists():
        print("Dataset already loaded. Skipping import.")
        return True
    try:
        with open("./review_dataset.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header if it exists
            for row in reader:
                try:
                    # Assuming CSV columns are in order corresponding to the model fields
                    (
                        ID,
                        Name,
                        City,
                        Category,
                        Ratings,
                        Rating_count,
                        Description,
                        Address,
                        Map_link,
                        Review_1,
                        Review_2,
                        Review_3,
                        openingHours_0_day,
                        openingHours_0_hours,
                        openingHours_1_day,
                        openingHours_1_hours,
                        openingHours_2_day,
                        openingHours_2_hours,
                        openingHours_3_day,
                        openingHours_3_hours,
                        openingHours_4_day,
                        openingHours_4_hours,
                        openingHours_5_day,
                        openingHours_5_hours,
                        openingHours_6_day,
                        openingHours_6_hours,
                    ) = row

                    sentiment_value = 1
                    # Create an instance of Dataset model and save it
                    res = Dataset.objects.create(
                        ID=ID,
                        Name=Name,
                        City=City,
                        Category=Category,
                        Ratings=Ratings,
                        Rating_count=Rating_count,
                        Description=Description,
                        Address=Address,
                        Map_link=Map_link,
                        Review_1=Review_1,
                        Review_2=Review_2,
                        Review_3=Review_3,
                        openingHours_0_day=openingHours_0_day,
                        openingHours_0_hours=openingHours_0_hours,
                        openingHours_1_day=openingHours_1_day,
                        openingHours_1_hours=openingHours_1_hours,
                        openingHours_2_day=openingHours_2_day,
                        openingHours_2_hours=openingHours_2_hours,
                        openingHours_3_day=openingHours_3_day,
                        openingHours_3_hours=openingHours_3_hours,
                        openingHours_4_day=openingHours_4_day,
                        openingHours_4_hours=openingHours_4_hours,
                        openingHours_5_day=openingHours_5_day,
                        openingHours_5_hours=openingHours_5_hours,
                        openingHours_6_day=openingHours_6_day,
                        openingHours_6_hours=openingHours_6_hours,
                    )
                    # If creation successful, print success message
                    print(f"Record with ID {ID} imported successfully.")
                except IntegrityError:
                    # If duplicate ID found, skip the record and continue with the next one
                    print(f"Skipping record with duplicate ID {ID}.")
                    continue
        DatasetLoaded.objects.create(is_loaded=True)
        return True
    except FileNotFoundError:
        print("File not found.")
        return False
