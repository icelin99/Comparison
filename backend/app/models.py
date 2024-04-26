from pydantic import BaseModel
from typing import List


class DatasetItem(BaseModel):
    id: int
    name: str

class TagItem(BaseModel):
    id: int
    name: str

class ModelItem(BaseModel):
    id: int
    name: str

class ModelListItem(BaseModel):
    id: int
    name: str
    answer: str
    score: float
    standard: str

class PageInfo(BaseModel):
    vqa_id: int
    question: str
    image_path: str
    tag: List[TagItem]
    model_list: List[ModelListItem]

class Page(BaseModel):
    page: int
    total_pages: int
    items: List[PageInfo]

def get_first_page(page = 1):
    index = page-1
    page_info = {
        "vqa_id": "0",
        "question": "this is a question",
        "image_path": "/xx/xx",
        "tag": [{
            "id": "1",
            "name": "tag 1"
        }, {
            "id": "2",
            "name": "tag 2"
        }],
        "model_list": [{
            "id": "1", # model id
            "name": "model name",
            "answer": "answer",
            "score": "null",
            "standard": "null", 
        }]
    }
    return page_info
