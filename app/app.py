import logging
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import re
from read_from_sheet import extract_phone_numbers_sheet
from page_review import handle_requests


app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/process_text', methods=['POST', 'OPTIONS'])
def process_text():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight request handled'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # Handle the POST request and extract phone numbers
        text1 = request.json['text1']
        text2 = request.json['text2']
        num_lists = request.json['num_lists']
        exclude_numbers = request.json['exclude_numbers']

        logging.info("Received a request to process text from IP: %s",
                     request.headers.get('X-Forwarded-For', request.remote_addr))

        phone_numbers1 = extract_phone_numbers(text1)
        phone_numbers_instructors = extract_phone_numbers_sheet()

        # Format the exclude_numbers
        formatted_exclude_numbers = format_phone_numbers(exclude_numbers)
        formatted_exclude_numbers_instructors = format_phone_numbers(phone_numbers_instructors)
        print(formatted_exclude_numbers_instructors)
        # Subtract the formatted_exclude_numbers_instructors from phone_numbers1
        subtracted_numbers, count_subtracted = subtract_phone_numbers(phone_numbers1, formatted_exclude_numbers + formatted_exclude_numbers_instructors)
        instructors_names = extract_text2_items(text2)  # Extract items from text2

        # Count the whole Whatsapp group
        total_count = count_unique_phone_numbers_and_names(text1)

        if num_lists > 0:
            divided_lists = divide_phone_numbers(subtracted_numbers, num_lists)  # Divide into num_lists lists
        elif len(instructors_names) > 0:
            divided_lists = divide_phone_numbers(subtracted_numbers, len(instructors_names))  # Divide into instructors_names lists
        else:
            num_lists = max(1, num_lists)  # Set num_lists to at least 1
            divided_lists = divide_phone_numbers(subtracted_numbers, num_lists)  # Divide into num_lists lists

        # Prepare the response
        response_data = {
            'num_phones': total_count+1,
            'phone_lists': divided_lists,
            'count_attendees': len(subtracted_numbers),
            'text2_items': instructors_names,
            'list2_length': len(instructors_names),
            'count_subtracted': count_subtracted  # Include the count of subtracted numbers in the response

        }

        logging.info("Processed the request successfully.")
        # Return the response
        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error processing text: {str(e)}"
        logging.error(error_message)
        return jsonify({'error': error_message}), 500


def count_unique_phone_numbers_and_names(input_text):
    # Use regular expressions to find all phone numbers and names
    phone_numbers = re.findall(r'(\+\d+[\d\s()-]+)', input_text)
    names = re.findall(r'[\u0590-\u05FF]+', input_text)

    # Remove duplicates from the phone numbers and names lists
    unique_phone_numbers = list(set(phone_numbers))
    unique_names = list(set(names))

    # Return the total count of unique phone numbers and names
    total_count = len(unique_phone_numbers) + len(unique_names)
    return total_count


def extract_phone_numbers(text):
    # Use regular expressions to extract phone numbers from the text
    phone_pattern = re.compile(r'(\+\d+[\d\s()-]+)')
    phone_numbers = phone_pattern.findall(text)
    phone_numbers = [''.join(phone) for phone in phone_numbers]

    # Remove duplicates using a set
    phone_numbers = list(set(phone_numbers))

    return phone_numbers

def subtract_phone_numbers(phone_numbers1, phone_numbers2):
    # Convert the phone_numbers2 list to a set for faster lookup
    phone_numbers2_set = set(phone_numbers2)

    # Use list comprehension to filter out numbers present in phone_numbers2
    subtracted_numbers = [number for number in phone_numbers1 if number not in phone_numbers2_set]

    # Calculate the count of subtracted numbers
    count_subtracted = len(phone_numbers1) - len(subtracted_numbers)

    return subtracted_numbers, count_subtracted

def divide_phone_numbers(phone_numbers, num_lists):
    # Calculate the number of phone numbers per list
    numbers_per_list = len(phone_numbers) // num_lists
    remainder = len(phone_numbers) % num_lists

    divided_lists = []

    # Divide the phone numbers into equal lists
    start = 0
    for i in range(num_lists):
        sublist_size = numbers_per_list
        if remainder > 0:
            sublist_size += 1
            remainder -= 1

        sublist = phone_numbers[start: start + sublist_size]
        divided_lists.append(sublist)

        start += sublist_size
    return divided_lists

def format_phone_numbers(phone_numbers):
    formatted_numbers = []
    for number in phone_numbers:
        # Ignore empty strings
        if not number:
            continue

        # Check if the number is already in the desired format
        if number.startswith('+972') and '-' in number:
            formatted_numbers.append(number)
        elif number.startswith('05') and '-' not in number:
            # Remove the leading '0' and add '+972' as prefix
            formatted_number = '+972 ' + number[1:]

            # Add '-' after 2 digits and another '-' after 3 more digits
            formatted_number = formatted_number[:7] + '-' + formatted_number[7:10] + '-' + formatted_number[10:]

            formatted_numbers.append(formatted_number)
        else:
            # Add '+' at the start and add space after every three characters
            formatted_number = '+' + number[:2] + ' ' + number[2:5] + ' ' + number[5:8] + ' ' + number[8:]
            formatted_numbers.append(formatted_number)

    return formatted_numbers

def extract_text2_items(text):
    # Split text2 into items based on newline characters
    items = text.strip().split('\n')

    return items

# Define a route to handle the page_review task
@app.route('/page_review', methods=['POST'])
def page_review():
    try:
        data = request.json
        success, message = handle_requests(data)  # Call the updated function

        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
