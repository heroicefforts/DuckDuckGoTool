import unittest

from duck_duck_go_photo_search import DuckDuckGoPhotoSearchSchema, DuckDuckGoPhotoSearchTool


class DuckDuckGoPhotoSearchTestCase(unittest.TestCase):
    def setUp(self):
        self.tool = DuckDuckGoPhotoSearchTool()

    def test_tool_name(self):
        self.assertEqual(self.tool.name, "DuckDuckGoPhotoSearch")
    
    def test_tool_args_schema(self):
        self.assertEqual(self.tool.args_schema, DuckDuckGoPhotoSearchSchema)
