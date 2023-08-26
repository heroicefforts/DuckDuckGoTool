import json
import requests
from itertools import islice
from typing import Type

from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool

# Const variables
DUCKDUCKGO_MAX_ATTEMPTS = 3
PHOTO_EXTRACTOR_MAX_ATTEMPTS = 2
MAX_PHOTOS_TO_SCRAPE = 3


class DuckDuckGoPhotoSearchSchema(BaseModel):
    query: str = Field(
        ...,
        description="The search query for duckduckgo search.",
    ),
    max_photos: int = Field(
        1,
        description="The maximum number of photos to return."
    )


class DuckDuckGoPhotoSearchTool(BaseTool):
    """
    Duck Duck Go Photo Search tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    # llm: Optional[BaseLlm] = None
    name = "DuckDuckGoPhotoSearch"
    description = (
        "A tool for performing a DuckDuckGo photo search and extracting photo images."
        "Input should be a search query and, optionally, the maximum number of photos to return (default max photos "
        "is 1)."
    )
    args_schema: Type[DuckDuckGoPhotoSearchSchema] = DuckDuckGoPhotoSearchSchema

    class Config:
        arbitrary_types_allowed = True

    def _execute(self, query: str, max_photos: int) -> list:

        """
        Execute the DuckDuckGo photo search tool.

        Args:
            query : The query to search for.

        Returns:
            Search result photo image bytes.
        """

        photo_links = self.get_duckduckgo_photo_links(query, max_photos)
        return self.download_images(photo_links)

    @staticmethod
    def get_duckduckgo_photo_links(query, max_photos):
        """
        Gets photo links from the duckduckgosearch python package
        Args:
            query : The query to search for.
            max_photos : The maximum number of photos to return.

        Returns:
            Returns photo links from the duckduckgosearch results
        """
        image_links = []
        attempts = 0

        while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
            if not query:  # checking if string is empty, if it is empty-> convert array to JSON object and return it;
                return json.dumps(image_links)

            with DDGS() as ddgs:
                ddgs_images_gen = ddgs.images(
                    query,
                    region="wt-wt",
                    safesearch="on",
                    size="Large",
                    color="color",
                    type_image="photo",
                    layout=None,
                    license_image=None,
                )
                search_results = list(islice(ddgs_images_gen, max_photos))
                image_links = [r['image'] for r in search_results]

            if search_results:  # if search result is populated,break as there is no need to attempt the search again
                break

            attempts += 1

        return image_links

    @staticmethod
    def download_images(image_links):
        """
        Downloads images from the duckduckgosearch python package
        Args:
            image_links : The image links to extract.

        Returns:
            Returns image bytes from the duckduckgosearch results
        """
        images = []

        if not image_links:
            return images

        attempts = 0
        for image_link in image_links:
            while attempts < PHOTO_EXTRACTOR_MAX_ATTEMPTS:
                response = requests.get(image_link)
                if response.status_code == 200:
                    images.append(response.content)
                    break

                attempts += 1
