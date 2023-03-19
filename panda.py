import csv
from datetime import datetime, timedelta

# Set path to CSV file
csv_path = '/Users/nicoleregondi/Desktop/Glovo/inventory_data.csv'

# Create dictionary to store inventory data
inventory_data = {}

# Open CSV file and read data into dictionary
with open(csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        store_id = row['store_id']
        product_id = row['product_id']
        inventory_data.setdefault(store_id, {})
        inventory_data[store_id].setdefault(product_id, [])
        inventory_data[store_id][product_id].append(row)

# Calculate inventory accuracy rate and stockout rate for each store
for store_id, products in inventory_data.items():
    total_products = 0
    total_stockouts = 0
    total_check_counts = 0
    total_check_time = timedelta()

    for product_id, inventory in products.items():
        last_inventory = inventory[-1]
        stock_on_hand_before = int(last_inventory['stock_on_hand_before'])
        stock_on_hand_after = int(last_inventory['stock_on_hand_after'])
        stock_count = int(last_inventory['stock_count'])
        total_products += 1
        if stock_on_hand_after == 0:
            total_stockouts += 1
        check_time = datetime.strptime(last_inventory['time_to_do_inventory'], '%H:%M:%S').time()
        total_check_time += timedelta(hours=check_time.hour, minutes=check_time.minute, seconds=check_time.second)
        total_check_counts += 1

    inventory_accuracy_rate = (total_products - total_stockouts) / total_products * 100
    stockout_rate = total_stockouts / total_products * 100
    avg_daily_check_time = total_check_time / total_check_counts
    avg_weekly_check_time = total_check_time / total_check_counts * 7
    avg_monthly_check_time = total_check_time / total_check_counts * 30

    print(f"Store ID: {store_id}")
    print(f"Inventory Accuracy Rate: {inventory_accuracy_rate:.2f}%")
    print(f"Stockout Rate: {stockout_rate:.2f}%")
    print(f"Avg. Daily Check Time: {avg_daily_check_time}")
    print(f"Avg. Weekly Check Time: {avg_weekly_check_time}")
    print(f"Avg. Monthly Check Time: {avg_monthly_check_time}")
    print()



# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Define the scope and credentials to access the Google Sheets API
# SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
# SERVICE_ACCOUNT_FILE = '/path/to/service_account.json'
# creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)

# # Define the ID of the Google Sheet to write data to
# SHEET_ID = 'your-sheet-id-here'

# # Create a client to interact with the Google Sheets API
# client = gspread.authorize(creds)

# # Open the sheet and select the first worksheet
# sheet = client.open_by_key(SHEET_ID).sheet1

# # Define the metrics to write to the sheet
# inventory_accuracy_rate = 0.95
# stockout_rate = 0.05
# daily_avg_time = '00:25:00'
# weekly_avg_time = '00:30:00'
# monthly_avg_time = '00:35:00'

# # Define the data to write to the sheet
# data = [
#     ['Inventory Accuracy Rate', inventory_accuracy_rate],
#     ['Stockout Rate', stockout_rate],
#     ['Daily Avg. Time to Do Inventory', daily_avg_time],
#     ['Weekly Avg. Time to Do Inventory', weekly_avg_time],
#     ['Monthly Avg. Time to Do Inventory', monthly_avg_time]
# ]

# # Write the data to the sheet
# sheet.insert_rows(data, 1)
