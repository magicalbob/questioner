import unittest
import os
import tempfile
import shutil
from answer import construct_prompt

class TestAnswer(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_path = tempfile.mkdtemp()
        self.test_files = [
            {'file1': 'test_file1.txt'},
            {'file2': 'test_file2.txt'}
        ]
        # Create fake files for testing
        with open(os.path.join(self.test_path, 'test_file1.txt'), 'w') as f:
            f.write("Content of test file 1")
        with open(os.path.join(self.test_path, 'test_file2.txt'), 'w') as f:
            f.write("Content of test file 2")

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_path)

    def test_construct_prompt(self):
        question = "What does this project do?"
        expected_output = (
            "My project contains these files:\n\n"
            "test_file1.txt:\nContent of test file 1\n\n"
            "test_file2.txt:\nContent of test file 2\n\n"
            "I want to know: What does this project do?"
        )
        result = construct_prompt(self.test_path, self.test_files, question)
        self.assertEqual(result.strip(), expected_output.strip())

    def test_file_not_found(self):
        non_existent_file = [{'file1': 'non_existent_file.txt'}]
        question = "What is the function of this file?"
        expected_file_path = os.path.join(self.test_path, 'non_existent_file.txt')
        expected_output = (
            "My project contains these files:\n\n"
            f"non_existent_file.txt: [File not found ({expected_file_path})]\n\n"
            "I want to know: What is the function of this file?"
        )
        result = construct_prompt(self.test_path, non_existent_file, question)
        self.assertEqual(result.strip(), expected_output.strip())

if __name__ == '__main__':
    unittest.main()
