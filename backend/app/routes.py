from fastapi import APIRouter, Query, HTTPException, UploadFile, File
from typing import Optional, List
from .database import Dataset, ModelName, Standard, Category, Tag, DataInfo, Result, get_category_by_dataset, get_tags_by_dataset_and_categories, get_filter_results, save_page_by_page
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
import uuid

router = APIRouter()

class TagRequest(BaseModel):
    datasetID: Optional[int] = None
    modelIDs: Optional[List[int]] = None
    categoryIDs: Optional[List[int]] = None

class FilterRequest(BaseModel):
    datasetID: int
    modelIDs: Optional[List[int]] = None
    tagIDs: Optional[List[int]] = None
    categoryIDs: Optional[List[int]] = None

class SaveRequest(BaseModel):
    data_info_id: int
    datasetID: int
    modelID: int
    score: Optional[float] = None
    standard: int
    tagIDs: Optional[List[int]] = None
    categoryIDs: Optional[List[int]] = None

class PathRequest(BaseModel):
    file: str
    type: str

@router.get("/")
def read_root():
    return "Hello World"

@router.get("/list/dataset/")
async def get_dataset_list():
    datasets = await Dataset.all()
    return [{"id": dataset.id, "name": dataset.name} for dataset in datasets]

@router.get("/list/model/")
async def get_model_list(datasetID: Optional[int] = None):
    if(datasetID):
        id = int(datasetID)
        print("dataset id",id)
        models = await ModelName.filter(dataset=id)
    else:
        models = await ModelName.all()
    return [{"id": model.id, "name": model.name} for model in models]

@router.get("/list/standard/")
async def get_standard_list():
    standards = await Standard.all()
    return [{"id": standard.id, "name": standard.value} for standard in standards]

@router.get("/list/category/")
# 参数允许为空
async def get_category_list(datasetID: Optional[int] = None, modelIDs: Optional[List] = Query(None) ):
    if(datasetID):
        id = int(datasetID)
        categories_list = await get_category_by_dataset(id)
    else:
        categories = await Category.all()
        categories_list = [{"id": category.id, "name": category.name} for category in categories]
    return categories_list

# 参数允许为空
@router.post("/list/tag/")
async def get_tag_list(request: TagRequest):
    datasetID = request.datasetID
    modelIDs = request.modelIDs
    categoryIDs = request.categoryIDs
    print("datasetID, modelIDs, categoryIDs:", datasetID, modelIDs, categoryIDs)
    try:
        # 假设这个函数需要实现，用于根据给定的ID获取标签列表
        tags = await get_tags_by_dataset_and_categories(datasetID, categoryIDs)
        print(tags)
        return tags
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="No tags found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/filter/")
# 参数允许为空
async def get_filter_list(request: FilterRequest):
    datasetID = request.datasetID
    modelIDs = request.modelIDs
    tagIDs = request.tagIDs
    categoryIDs = request.categoryIDs
    print("datasetID, modelIDs, tagIDs, categoryIDs:", datasetID, modelIDs, tagIDs, categoryIDs)
    output = await get_filter_results(datasetID,modelIDs, tagIDs,categoryIDs)
    return {"page_count":output["total_page"], "page_info":output["page_info"]}

@router.post("/page/{page_id}/")
async def get_page_by_page_id(page_id: int, request: FilterRequest):
    datasetID = request.datasetID
    modelIDs = request.modelIDs
    tagIDs = request.tagIDs
    categoryIDs = request.categoryIDs
    print("page id", page_id,"datasetID, modelIDs, tagIDs, categoryIDs:", datasetID, modelIDs, tagIDs, categoryIDs)
    output = await get_filter_results(datasetID,modelIDs, tagIDs,categoryIDs, page_id)
    return {"page_count":output["total_page"], "page_info":output["page_info"]}


@router.post("/save/{page_id}/")
async def save_by_page_id(page_id: int, request: SaveRequest):
    print(f"Received data: {request}")
    data_info_id = request.data_info_id
    datasetID = request.datasetID
    modelID = request.modelID
    tagIDs = request.tagIDs
    categoryIDs = request.categoryIDs
    score = request.score
    standard = request.standard
    message = await save_page_by_page(page_id,data_info_id,datasetID,modelID,standard,score,tagIDs,categoryIDs)
    return {"message": message}

@router.post("/upload-file/")
async def upload_json(file: UploadFile = File(...)):
    print("file ok")
    contents = await file.read()
    return {"filename": file.filename, "content_type": file.content_type}

@router.post("/upload-file-path/")
async def upload_json_path(request: PathRequest):
    print("file path ok",request.file)
    if(request.type == 'dataset'):
        print("dataset")
    elif(request.type == "model"):
        print("model")
    return {"message": "File uploaded sucessfully"}