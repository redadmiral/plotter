from pydantic import BaseModel
from typing import List

class GerbilData(BaseModel):
    type: str
    matching: str
    annotator: List[str]
    dataset: List[str]
