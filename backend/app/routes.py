from fastapi import APIRouter, Query
from typing import Optional, List
from .models import get_first_page

router = APIRouter()


@router.get("/")
def read_root():
    return "Hello World"

@router.get("/list/dataset/")
def get_dataset_list():
    datasets = [{
        "id": "1",
        "name": "dataset 1"
    },{
        "id": "2",
        "name": "daatset 2"
    }]
    return datasets

@router.get("/list/model/")
def get_model_list():
    models = [{
        "id": "1",
        "name": "model 1"
    },{
        "id": "2",
        "name": "model 2"
    }]
    return models

@router.get("/list/standard/")
def get_standard_list():
    standards = [{
        "id": "1",
        "name": "3"
    }, {
        "id": "2",
        "name": "5"
    }]
    return standards

@router.get("/list/category/")
# 参数允许为空
def get_category_list(datasetID: int = Query(), modelIDs: List = Query([])):
    categories = [{
        "id": "1",
        "name": "category 1"
    }, {
        "id": "2",
        "name": "category 2"
    }]
    return categories

@router.get("/list/tag/")
# 参数允许为空
def get_tag_list(datasetID: int = Query(), modelIDs: List = Query([])):
    tags = [{
        "id": "1",
        "name": "tag 1"
    }, {
        "id": "2",
        "name": "tag 2"
    }]
    return tags

@router.get("/filter/")
# 参数允许为空
def get_filter_list(datasetID: int = Query(..., ge=1), modelIDs: List = Query(..., min_length=1), tagIDs: List = Query([]), categoryIDs: List = Query([])):
    id_list = [1,2,3,4,5,6]
    page_info = get_first_page(1)
    return {"id_list": id_list, "page_info": page_info}

@router.get("/page/{page_id}")
def get_page_by_page_id(page_id: int):
    page_info = get_first_page(page_id)
    return page_info

@router.post("/save/{page_id}/")
def save_by_page_id(page_id: int, model_id: int, score: float, standard: str = None):
    return {"message": "saved successfully"}
    
