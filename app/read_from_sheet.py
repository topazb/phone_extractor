import gspread
from oauth2client.service_account import ServiceAccountCredentials

def extract_phone_numbers_sheet():
    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    # Authorize the client
    client = gspread.authorize(credentials)

    # Open the Google Sheet by its title
    spreadsheet = client.open('פרטי מדריכים אתגר 22')

    # Get data from sheet 1
    sheet1 = spreadsheet.sheet1
    data_sheet1 = sheet1.get_all_values()

    # Extract and trim phone numbers from sheet 1
    phone_numbers = []
    for row in data_sheet1[1:]:  # Start from the second row to skip the header row
        phone_number = row[2]  # Assuming the phone number is in the third column (index 2)
        phone_number = phone_number.replace("טלפון", "").replace("-", "").strip()
        if phone_number:  # Add only non-empty phone numbers
            phone_numbers.append(phone_number)

    # Get data from sheet 2
    sheet2 = spreadsheet.get_worksheet(1)  # Index 1 corresponds to the second sheet (0-indexed)
    data_sheet2 = sheet2.get_all_values()

    # Extract and trim phone numbers from sheet 2
    for row in data_sheet2[1:]:
        phone_number = row[1]  # Assuming the phone number is in the second column (index 1)
        phone_number = phone_number.replace("טלפון", "").replace("-", "").strip()
        if phone_number:  # Add only non-empty phone numbers
            phone_numbers.append(phone_number)

    return phone_numbers

# Call the function to extract phone numbers
phone_numbers = extract_phone_numbers_sheet()
