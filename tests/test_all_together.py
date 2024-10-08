import unittest
from unittest.mock import patch, MagicMock
import all_together

class TestAllTogether(unittest.TestCase):

    @patch('all_together.os.getenv')
    @patch('all_together.subprocess.run')
    @patch('all_together.ask_chatgpt')
    def test_main_flow(self, mock_ask_chatgpt, mock_subprocess, mock_getenv):
        # Mock return values
        mock_getenv.return_value = "fake_api_key"
        mock_subprocess.return_value.stdout = "meta-question"
        mock_ask_chatgpt.side_effect = [
            '{"file1": "file1.txt", "file2": "file2.txt"}',  # First call
            '{"file1": "file1.txt", "file2": "file2.txt"}',  # Second call
            'Final Answer from ChatGPT'  # Final answer
        ]

        # Run the main function
        all_together.main()

        # Assertions
        mock_subprocess.assert_called()  # Ensure subprocess was called
        self.assertEqual(mock_ask_chatgpt.call_count, 3)  # Ensure the correct number of calls to ask_chatgpt
       
    # Additional tests for specific functions can go here
    # e.g., test_save_to_temp_file, test_validate_json, etc.

if __name__ == '__main__':
    unittest.main()
