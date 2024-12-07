import unittest
import tempfile
import os
from markdown_it import MarkdownIt
from rich.console import Console
from utils import parse_markdown

class TestParseMarkdown(unittest.TestCase):

    def create_temp_file(self, content):
        temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8')
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def test_single_heading_with_content(self):
        content = "# Heading 1\nThis is some content."
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        self.assertEqual(result, {"Heading 1": "This is some content."})
        os.unlink(file_path)

    def test_multiple_headings_same_level(self):
        content = "# Heading 1\nContent 1\n\n# Heading 2\nContent 2\n\n# Heading 3\nContent 3"
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        expected = {
            "Heading 1": "Content 1",
            "Heading 2": "Content 2",
            "Heading 3": "Content 3"
        }
        self.assertEqual(result, expected)
        os.unlink(file_path)

    def test_multiple_headings_nested(self):
        content = "# Heading 1\nContent 1\n\n## Heading 2\nContent 2\n\n# Heading 3\nContent 3"
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        expected = {
            "Heading 1": "Content 1",
            ("Heading 1", "Heading 2"): "Content 2",
            "Heading 3": "Content 3"
        }
        self.assertEqual(result, expected)
        os.unlink(file_path)

    def test_multiple_headings_double_nesting(self):
        content = "# Heading 1\nContent 1\n\n## Heading 2\nContent 2\n\n### Heading 3\nContent 3\n\n# Heading 4\nContent 4"
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        print(result)
        expected = {
            "Heading 1": "Content 1",
            ("Heading 1", "Heading 2"): "Content 2",
            ("Heading 1", "Heading 2", "Heading 3"): "Content 3",
            "Heading 4": "Content 4"
        }
        self.assertEqual(result, expected)
        os.unlink(file_path)

    def test_multiple_headings_triple_nesting(self):
        content = "# Heading 1\nContent 1\n\n## Heading 2\nContent 2\n\n### Heading 3\nContent 3\n\n### Heading 3a\nContent 3a\n\n# Heading 4\nContent 4"
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        print(result)
        expected = {
            "Heading 1": "Content 1",
            ("Heading 1", "Heading 2"): "Content 2",
            ("Heading 1", "Heading 2", "Heading 3"): "Content 3",
            ("Heading 1", "Heading 2", "Heading 3a"): "Content 3a",
            "Heading 4": "Content 4"
        }
        self.assertEqual(result, expected)
        os.unlink(file_path)

    def test_multiple_headings_nesting_up_then_down(self):
        content = """
# Heading 1
Content 1

## Heading 2
Content 2

### Heading 3
Content 3

#### Heading 4
Content 4

### Heading 3a
Content 3a

# Heading 1a
Content 1a
"""
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        print(result)
        expected = {
            "Heading 1": "Content 1",
            ("Heading 1", "Heading 2"): "Content 2",
            ("Heading 1", "Heading 2", "Heading 3"): "Content 3",
            ("Heading 1", "Heading 2", "Heading 3", "Heading 4"): "Content 4",
            ("Heading 1", "Heading 2", "Heading 3a"): "Content 3a",
            "Heading 1a": "Content 1a"
        }
        self.assertEqual(result, expected)
        os.unlink(file_path)

    def test_heading_without_content(self):
        content = "# Heading 1\n\n## Heading 2\nContent 2"
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        expected = {
            ("Heading 1", "Heading 2"): "Content 2"
        }
        print(result)
        self.assertEqual(result, expected)
        os.unlink(file_path)

    # def test_content_with_multiple_paragraphs(self):
    #     content = "# Heading 1\nParagraph 1\n\nParagraph 2\n\n# Heading 2\nContent 2"
    #     file_path = self.create_temp_file(content)
    #     result = parse_markdown(file_path)
    #     expected = {
    #         "Heading 1": "Paragraph 1\n\nParagraph 2",
    #         "Heading 2": "Content 2"
    #     }
    #     print(result)
    #     self.assertEqual(result, expected)
    #     os.unlink(file_path)

    def test_empty_file(self):
        content = ""
        file_path = self.create_temp_file(content)
        result = parse_markdown(file_path)
        self.assertEqual(result, {})
        os.unlink(file_path)


    # def test_file_with_only_headings(self):
    #     content = "# Heading 1\n## Heading 2\n### Heading 3"
    #     file_path = self.create_temp_file(content)
    #     result = parse_markdown(file_path)
    #     expected = {
    #         "Heading 1": "",
    #         "Heading 2": "",
    #         "Heading 3": ""
    #     }
    #     self.assertEqual(result, expected)
    #     os.unlink(file_path)

if __name__ == '__main__':
    unittest.main()