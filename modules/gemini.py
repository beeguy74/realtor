from typing import List
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, Candidate, Schema
from dotenv import load_dotenv
from os import getenv

import logging

load_dotenv()



logger = logging.getLogger(__name__)

class Gemini:
    def __init__(self):
        self.client = genai.Client(api_key=getenv("GEMINI_API_KEY", ""))
        self.model_id = "gemini-2.0-flash"
        self.google_search_tool = Tool(
            google_search=GoogleSearch()
        )
        
    def generate(self, query: str, config=GenerateContentConfig(
                temperature=1,
                max_output_tokens=4096,
            )) -> str:
        """
        Simple response generation function, withou any tools
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=query,
            config=config
        )
        return response.candidates[0].content.parts[0].text
    
    
    def chat(self, messages: List[str]) -> str:
        """
        Chat function, for multiple messages
        """
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=messages,
            config=GenerateContentConfig(
                temperature=1,
                max_output_tokens=4096,
            )
        )
        return response.candidates[0].content.parts[0].text


    def find_videos(self, car_model: str) -> dict[str, str]:
        """
        gets car_model and generates and searches for videos about the car on Doug Demuro's YouTube channel
        Returns dict with text and chunks contains title(domain source) and uri of the videos
        """
        prompt = f'''I need video about the most recent model of {car_model} car.
        Make sure not to include video that reviews list of similar cars.
        '''
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=GenerateContentConfig(
                tools=[self.google_search_tool],
                system_instruction="""You are the search assistant that helps to find videos about the asked car on YouTube platform.
                Find trending and interesting videos about cars, including reviews, test drives, modifications, and industry news. 
                Prioritize recent and engaging videos that match the interests of car enthusiasts.""",
                temperature=1,
                max_output_tokens=1024,
            )
        )

        grounding_chunks = []
        text = []
        for each in response.candidates:
            each: Candidate
            if each.content.parts:
                text.append(each.content.parts[0].text)
            if hasattr(each, "grounding_metadata") and each.grounding_metadata:
                for chunk in each.grounding_metadata.grounding_chunks:
                    if chunk.web.title == "youtube.com":
                        grounding_chunks.append(chunk)
                    else:
                        print("Bad source : {}".format(chunk.web.title))
            else:
                print("Unsuccessful")
                return None
        # To get grounding metadata as web content.
        # print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
        return {"text": text, "chunks": grounding_chunks}
    


if __name__ == "__main__":
    gemini = Gemini()
    
    print(gemini.generate("what is Lune?"))

    # Does not work with google search tool
    # responseSchema = Schema(
    #     type=Type.OBJECT,
    #     enum=[],
    #     required=["videos"],
    #     properties={
    #         "videos": Schema(
    #             type=Type.ARRAY,
    #             items=Schema(
    #                 type=Type.OBJECT,
    #                 enum=[],
    #                 required=["video"],
    #                 properties={
    #                     "video": Schema(
    #                         type=Type.OBJECT,
    #                         enum=[],
    #                         required=["name", "url", "author"],
    #                         properties={
    #                             "name": Schema(
    #                                 type=Type.STRING,
    #                             ),
    #                             "url": Schema(
    #                                 type=Type.STRING,
    #                             ),
    #                             "author": Schema(
    #                                 type=Type.STRING,
    #                             ),
    #                         },
    #                     ),
    #                 },
    #             ),
    #         ),
    #     },
    # )