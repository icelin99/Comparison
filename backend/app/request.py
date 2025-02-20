from pydantic import BaseModel
from typing import Optional, List, Union

class CategoryRequest(BaseModel):
    datasetID: Optional[int] = None
    modelIDs: Optional[List[int]] = None
    tagIDs: Optional[List[int]] = None

class TagRequest(BaseModel):
    datasetID: Optional[int] = None
    modelIDs: Optional[List[int]] = None
    categoryIDs: Optional[List[int]] = None

class FilterRequest(BaseModel):
    datasetID: int
    modelIDs: Optional[List[int]] = None
    standard: int
    tagIDs: Optional[List[int]] = None
    categoryIDs: Optional[List[int]] = None
    score: Optional[float] = None

class FilterRequestByID(BaseModel):
    modelIDs: Optional[List[int]]
    standard: int
    score: Optional[float] = None

class ModelListGet(BaseModel):
    modelID: int
    model_name: str
    answer: str
    score: float

class ModelListSave(BaseModel):
    modelID: int
    score: Union[float, None] = None
    standard: int

class SaveRequest(BaseModel):
    data_info_id: int
    datasetID: int
    modelList: List[ModelListSave]

class PathRequest(BaseModel):
    file: str
    type: str

class ScoreFileRequest(BaseModel):
    filename: str
    question: str
    score: Optional[float] = None
    category: Optional[str] = None
    tag: Optional[List[str]] = None
    result: Optional[str] = None

class EditAnswerRequest(BaseModel):
    datainfoID: int
    ref_answer: str

class DeleteDataset(BaseModel):
    datasetID: int

class DeleteResult(BaseModel):
    datasetID: int
    modelID: int

class AccuracyRequest(BaseModel):
    datasetID: int
    modelIDs: List[int]
    standard: int

class ChangeModelName(BaseModel):
    datasetID: int
    modelID: int
    modelname: str

class ScoreDownload(BaseModel):
    datasetID: int
    modelIDs: List[int]
    standard: int