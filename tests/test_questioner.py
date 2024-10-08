import unittest
import os
from questioner import get_file_structure, construct_meta_question

class TestQuestioner(unittest.TestCase):

    def test_get_file_structure(self):
        # Assuming you have a test directory structure set up.
        test_dir = './test_project'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'file1.txt'), 'w') as f:
            f.write("This is a test file.")
        
        file_structure = get_file_structure(test_dir)
        self.assertIn('file1.txt', file_structure)

        # Clean up
        os.remove(os.path.join(test_dir, 'file1.txt'))
        os.rmdir(test_dir)

    def test_construct_meta_question(self):
        file_structure = ['file1.txt', 'file2.txt']
        user_question = "What does this project do?"
        expected_question = (
            "I have the following project structure:\n\nfile1.txt\nfile2.txt\n\n"
            "The user wants to know: 'What does this project do?'. "
            "Which files from the project do you need to look at to answer the user's question? "
            "Please answer in JSON like this [{'file1': 'name_of_file1'}, {'file2': 'name_of_file2'} ... {'fileN': 'name_of_fileN'}]. It is important that keys always start with file."
        )
        result = construct_meta_question(file_structure, user_question)
        self.assertEqual(result.strip(), expected_question.strip())

if __name__ == '__main__':
    unittest.main()
