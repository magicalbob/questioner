import unittest
import os
from questioner import get_file_structure, construct_meta_question

class TestQuestioner(unittest.TestCase):

    def setUp(self):
        self.test_dir = './test_project'
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, 'file1.txt'), 'w') as f:
            f.write("This is a test file.")

    def tearDown(self):
        # Make sure to clean up test directory
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_get_file_structure(self):
        file_structure = get_file_structure(self.test_dir)
        self.assertIn('file1.txt', file_structure)
        self.assertEqual(len(file_structure), 1)  # Verify only one file

    def test_construct_meta_question(self):
        self.maxDiff = None
        file_structure = ['file1.txt', 'file2.txt']
        user_question = "What does this project do?"
        expected_question = (
            "I have the following project structure:\n\nfile1.txt\nfile2.txt\n\n"
            "The user wants to know: 'What does this project do?'. Which files from the project do you need to look at to answer the user's question? "
            "Please answer in JSON like this [{'file1': 'name_of_file1'}, {'file2': 'name_of_file2'} ... {'fileN': 'name_of_fileN'}]. It is important that keys always start with file."
        )
        result = construct_meta_question(file_structure, user_question)
        self.assertEqual(result.strip(), expected_question.strip())

    def test_empty_directory(self):
        # Test when directory has no files
        empty_dir = './empty_test_project'
        os.makedirs(empty_dir, exist_ok=True)
        file_structure = get_file_structure(empty_dir)
        self.assertEqual(file_structure, [])  # No files should result in an empty list

        # Clean up
        os.rmdir(empty_dir)

if __name__ == '__main__':
    unittest.main()
