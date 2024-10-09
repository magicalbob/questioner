import unittest
from unittest.mock import patch, MagicMock
import sys
import alltogether

class TestAllTogether(unittest.TestCase):

    @patch('alltogether.os.getenv')
    @patch('alltogether.subprocess.run')
    @patch('alltogether.ask_chatgpt')
    @patch('sys.argv', ['alltogether.py', '--path', 'fake_path', '--question', 'fake_question'])  # Mock sys.argv
    def test_main_flow(self, mock_ask_chatgpt, mock_subprocess, mock_getenv):
        # Mock return values
        mock_getenv.return_value = "fake_api_key"
        mock_subprocess.return_value.stdout = "meta-question"
        mock_ask_chatgpt.side_effect = [
            [{"file1": "file1.txt", "file2": "file2.txt"}],  # First call should return a list of dicts
            [{"file1": "file1.txt", "file2": "file2.txt"}],  # Second call
            "Final Answer from ChatGPT"  # Final answer can remain a string
        ]

        # Run the main function
        alltogether.main()

        # Assertions
        mock_subprocess.assert_called()  # Ensure subprocess was called
        self.assertEqual(mock_ask_chatgpt.call_count, 3)  # Ensure the correct number of calls to ask_chatgpt

if __name__ == '__main__':
    unittest.main()
