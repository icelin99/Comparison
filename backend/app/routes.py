from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form
from typing import Optional, List
from .database import Dataset, ModelName, Standard, Category, Tag, DataInfo, Result
from .db_query import get_tags_by_dataset_and_categories, get_filter_results, save_page_by_page, read_file, fetch_save_file, get_categories, get_tags, update_dataset_by_path, update_result_by_path,update_score_by_path, save_ref_answer, del_dataset, del_result, get_accuracy_table, fetch_save_dataset, change_modelname, get_filter_result_plus, get_info_by_datainfo_id
from tortoise.exceptions import DoesNotExist
from .request import TagRequest, FilterRequest, SaveRequest, PathRequest, ScoreFileRequest, CategoryRequest, EditAnswerRequest, DeleteDataset, DeleteResult, AccuracyRequest, ChangeModelName, ScoreDownload, FilterRequestByID
from fastapi.responses import FileResponse
import os
import uuid
import base64

router = APIRouter()

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
    seen_values = set()
    unique_standards = []

    for standard in standards:
        if standard.value not in seen_values:
            seen_values.add(standard.value)
            unique_standards.append({"id": standard.id, "name": standard.value})
    
    return unique_standards


@router.post("/list/category/")
# 参数允许为空
async def get_category_list(request: CategoryRequest):
    print("get category list", request.datasetID, request.modelIDs)
    if request.datasetID and request.modelIDs and len(request.modelIDs) > 0:
        categories_list = await get_categories(request.datasetID, request.modelIDs, request.tagIDs)
        return categories_list
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
    if datasetID and modelIDs and len(modelIDs) > 0:
        tags_list = await get_tags(datasetID, modelIDs, categoryIDs)
        return tags_list
    else:
        tags = await Tag.all()
        tags_list = [{"id": tag.id, "name": tag.name} for tag in tags]
        return tags_list

@router.post("/filter/")
# 参数允许为空
async def get_filter_list(request: FilterRequest):
    datasetID = request.datasetID
    modelIDs = request.modelIDs
    standard = request.standard
    tagIDs = request.tagIDs
    categoryIDs = request.categoryIDs
    score = request.score
    print("datasetID, modelIDs, tagIDs, categoryIDs score:", datasetID, modelIDs, tagIDs, categoryIDs,score)
    output = None
    if score is None:
        output = await get_filter_results(datasetID,modelIDs, standard,tagIDs,categoryIDs)
    else:
        output = await get_filter_result_plus(datasetID,modelIDs,standard,tagIDs,categoryIDs,score)
    return {"page_count":output["total_page"], "page_info":output["page_info"],"data_info_list": output["data_info_list"]}

@router.post("/page/{datainfo_id}/")
async def get_page_by_page_id(datainfo_id:int, request: FilterRequestByID):
    modelIDs = request.modelIDs
    standard = request.standard
    score = request.score
    print("page id", datainfo_id,", modelIDs, score:",  modelIDs,score)
    output = await get_info_by_datainfo_id(datainfo_id,modelIDs, standard,score)
    return {"page_info":output}

@router.post("/save/{page_id}/")
async def save_by_page_id(page_id: int, request: SaveRequest):
    print(f"Received data: {request}")
    data_info_id = request.data_info_id
    datasetID = request.datasetID
    modelList = request.modelList
    succ_count = 0

    for model in modelList:
        modelID = model.modelID
        score = model.score
        standard = model.standard
        message = await save_page_by_page(page_id,data_info_id,datasetID,modelID,standard,score)
        if message == "save successfully!":
            succ_count +=1
    if succ_count == len(modelList):
        return {"message": "save successfully!"}
    else:
        return {"message": "save failed!"}

@router.post("/upload-file/")
async def upload_json(request: PathRequest):
    return await read_file(request.file, request.type)

@router.post("/upload-file-path/")
async def upload_json_path(request: PathRequest):
    print("file path ok",request.file,request.type)
    if(request.type == 'dataset'):
        return await update_dataset_by_path(request.file)
    elif(request.type == "result"):
        return await update_result_by_path(request.file)
    elif(request.type == "score"):
        return await update_score_by_path(request.file)
    else:
        return {"error":"unknwon error"}


@router.post("/fetch/file/")
async def fetch_file(request: ScoreDownload):
    res = await fetch_save_file(request.datasetID, request.modelIDs, request.standard)
    return res
    
@router.get("/fetch/dataset/")
async def fetch_dataset(datasetID: int):
    print(datasetID)
    res = await fetch_save_dataset(datasetID)
    return res

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_dir = os.path.abspath('downloads')
    file_path = os.path.join(file_dir, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.post("/edit-answer/")
async def edit_answer(request: EditAnswerRequest):
    ans = await save_ref_answer(request.datainfoID, request.ref_answer)
    return ans

@router.post("/delete-dataset/")
async def delete_dataset(request: DeleteDataset):
    res = await del_dataset(request.datasetID)
    print(res)
    return res

@router.post("/delete-result/")
async def delete_result(request: DeleteResult):
    res = await del_result(request.datasetID, request.modelID)
    print(res)
    return res

@router.post("/accuracy/")
async def get_accuracy(request: AccuracyRequest):
    res = await get_accuracy_table(request.datasetID, request.modelIDs, request.standard)
    return res

@router.post("/edit-modelname/")
async def change_model_name(request: ChangeModelName):
    res = await change_modelname(request.datasetID, request.modelID, request.modelname)
    return res