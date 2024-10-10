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
            '[{"file1": "file1.txt"}, {"file2": "file2.txt"}]',  # JSON response
            '[{"file1": "file1.txt"}, {"file2": "file2.txt"}]',  # JSON response
            "Final Answer from ChatGPT"  # Final answer can remain a string
        ]

        # Run the main function
        alltogether.main()

        # Assertions
        mock_subprocess.assert_called()  # Ensure subprocess was called
        self.assertEqual(mock_ask_chatgpt.call_count, 2)  # Ensure the correct number of calls to ask_chatgpt

    @patch('alltogether.os.getenv', return_value='fake_api_key')
    @patch('alltogether.subprocess.run')
    @patch('time.sleep', return_value=None)  # Skip actual sleep
    @patch('alltogether.openai.chat.completions.create', side_effect=Exception("API Error"))
    @patch('sys.argv', ['alltogether.py', '--path', 'fake_path', '--question', 'fake_question'])
    def test_api_error_handling(self, mock_argv, mock_create, mock_sleep, mock_subprocess, mock_getenv):
        mock_subprocess.return_value.stdout = "meta-question"

        with self.assertRaises(Exception) as context:
            alltogether.main()

        self.assertIn("API is overloaded", str(context.exception))

if __name__ == '__main__':
    unittest.main()
