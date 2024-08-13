import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up logging
logging.basicConfig(level=logging.DEBUG)


def extract_phone_numbers_sheet():
    # Define the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    try:
        # Authorize the client
        client = gspread.authorize(credentials)

        # Open the Google Sheet by its title
        spreadsheet = client.open('פרטי מדריכים אתגר 22')
        logging.debug("Successfully connected to the Google Sheet")

        # Function to clean and validate phone numbers
        def clean_phone_number(phone_number):
            if phone_number:
                phone_number = phone_number.replace("טלפון", "").replace("-", "").strip()
                return phone_number if phone_number and phone_number.isdigit() else None
            return None

        # Function to extract phone numbers from a given sheet
        def extract_numbers_from_sheet(sheet, column_index):
            phone_numbers = []
            try:
                data = sheet.get_all_values()
                for row in data[1:]:  # Skip the header row
                    phone_number = clean_phone_number(row[column_index])
                    if phone_number:
                        phone_numbers.append(phone_number)
            except Exception as e:
                logging.error(f"Error processing sheet: {e}")
                return []
            return phone_numbers

        # Extract phone numbers from sheet 1
        phone_numbers = extract_numbers_from_sheet(spreadsheet.sheet1, 2)

        # Extract phone numbers from sheet 2
        sheet2 = spreadsheet.get_worksheet(1)
        more_phone_numbers = extract_numbers_from_sheet(sheet2, 1)

        # Combine phone numbers from both sheets
        if more_phone_numbers:  # Check if more_phone_numbers is not None or empty
            phone_numbers.extend(more_phone_numbers)

        logging.debug(f"Extracted phone numbers: {phone_numbers}")
        return phone_numbers

    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return []


# Run the function
phone_numbers = extract_phone_numbers_sheet()

if phone_numbers:
    logging.debug(f"Final phone numbers list: {phone_numbers}")
else:
    logging.error("No phone numbers were extracted.")
