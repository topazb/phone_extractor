from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

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

        phone_numbers1 = extract_phone_numbers(text1)
        phone_numbers2 = extract_phone_numbers(text2)

        # Format the exclude_numbers
        formatted_exclude_numbers = format_phone_numbers(exclude_numbers)

        # Subtract the formatted_exclude_numbers from phone_numbers1
        phone_numbers1 = subtract_phone_numbers(phone_numbers1, formatted_exclude_numbers)

        # Subtract the phone numbers in text 2 from formatted_exclude_numbers
        active_instructors = subtract_phone_numbers(phone_numbers2, formatted_exclude_numbers)

        if num_lists > 0:
            divided_lists = divide_phone_numbers(phone_numbers1, num_lists)  # Divide into num_lists lists

        # Update divided_lists if active_instructors is not empty
        elif len(active_instructors) > 0:
            divided_lists = divide_phone_numbers(phone_numbers1, len(active_instructors))

        # Update num_lists if it is 0 or active_instructors is empty
        else:
            num_lists = max(1, num_lists)  # Set num_lists to the length of active_instructors or at least 1
            divided_lists = divide_phone_numbers(phone_numbers1, num_lists)  # Divide into num_lists lists

        # Prepare the response
        response_data = {
            'num_phones': len(phone_numbers1)+1,
            'phone_lists': divided_lists,
            'list2_length': len(phone_numbers2),
            'active_instructors_length': len(active_instructors),
            'active_instructors': active_instructors
        }
        # Return the response
        return jsonify(response_data)

    except Exception as e:
        error_message = f"Error processing text: {str(e)}"
        return jsonify({'error': error_message}), 500


def extract_phone_numbers(text):
    # Use regular expressions to extract phone numbers from the text
    phone_pattern = re.compile(r'(\+\d+[\d\s()-]+)')
    phone_numbers = phone_pattern.findall(text)
    phone_numbers = [''.join(phone) for phone in phone_numbers]

    # Remove duplicates using a set
    phone_numbers = list(set(phone_numbers))

    return phone_numbers

def subtract_phone_numbers(phone_numbers1, phone_numbers2):
    # Subtract phone numbers in phone_numbers2 from phone_numbers1
    subtracted_numbers = list(set(phone_numbers1) - set(phone_numbers2))

    return subtracted_numbers

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
        # Remove the leading '0' and add '+972' as prefix
        formatted_number = '+972 ' + number[1:]

        # Add '-' after 2 digits and another '-' after 3 more digits
        formatted_number = formatted_number[:7] + '-' + formatted_number[7:10] + '-' + formatted_number[10:]

        formatted_numbers.append(formatted_number)
        print(formatted_number)

    return formatted_numbers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
