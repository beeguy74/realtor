from modules.DatabaseManager import DatabaseManager
from modules.gemini import Gemini
from modules.processor import DataProcessor
from google.genai.types import Schema, GenerateContentConfig
from pydantic import BaseModel
import json

class AdResponse(BaseModel):
    subject: str
    body: str


def translate():
    db_manager = DatabaseManager()
    
    # Initialize data processor
    processor = DataProcessor(db_manager)
    ads = processor.get_recent_ads(5)
    config = GenerateContentConfig(
        temperature=0.8,
        response_schema=AdResponse,
        response_mime_type="application/json"
    )
    gemini = Gemini()
    for _, ad in enumerate(ads):
        try:
            prompt = f"Translate this annonce in english: the anonce's title:'{ad.subject}'; 'the anonce body: {ad.body}'"
            resp = gemini.generate(prompt, config)
            dic = json.loads(resp)
            if resp and dic.get("subject", "") and dic.get("body", ""):
                dic["translated"] = True
                processor._update_ad_fields(ad, dic, None)
                print(f"ad {ad.id} translated!")
            else:
                print(f"ad {ad.id} failed translate!")
        except Exception as e:
            print(f"ERROR {e}")
            break
        
        
if __name__=="__main__":
    translate()