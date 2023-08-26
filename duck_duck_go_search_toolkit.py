from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit
from duck_duck_go_search import DuckDuckGoSearchTool
from duck_duck_go_photo_search import DuckDuckGoPhotoSearchTool


class DuckDuckGoToolkit(BaseToolkit, ABC):
    name: str = "DuckDuckGo Search Toolkit"
    description: str = "Toolkit containing tools for performing DuckDuckGo search and extracting photos, snippets " \
                       "and webpages"

    def get_tools(self) -> List[BaseTool]:
        return [DuckDuckGoSearchTool(), DuckDuckGoPhotoSearchTool()]

    def get_env_keys(self) -> List[str]:
        return [
            # Add more config keys specific to your project
        ]
