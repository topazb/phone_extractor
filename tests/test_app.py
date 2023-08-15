import unittest
import requests


class TestApp(unittest.TestCase):
    def setUp(self):
        # Set up the base URL for the Flask app
        self.base_url = 'http://localhost:5000'

    def test_process_text_endpoint(self):
        # Test case 1: Valid input data
        data = {
            'text1': 'Text with phone number +972 123456789 and +972 987654321',
            'text2': 'Instructor 1\nInstructor 2',
            'num_lists': 2,
            'exclude_numbers': ['+972987654321']
        }
        response = requests.post(f'{self.base_url}/process_text', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('num_phones', response.json())
        self.assertIn('phone_lists', response.json())
        self.assertIn('text2_items', response.json())
        self.assertIn('list2_length', response.json())
        self.assertIn('count_subtracted', response.json())

        # Test case 2: Invalid input data (missing 'text1')
        data = {
            'text2': 'Instructor 1\nInstructor 2',
            'num_lists': 2,
            'exclude_numbers': ['+972987654321']
        }
        response = requests.post(f'{self.base_url}/process_text', json=data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.json())

        # Add more test cases as needed...


if __name__ == '__main__':
    unittest.main()
