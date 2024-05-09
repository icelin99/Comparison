from pydantic import BaseModel, Field
from typing import List
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from tortoise.functions import Count
import os
import json
import re
import base64


class Dataset(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    related_models = fields.ReverseRelation["ModelName"]

class ModelName(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    dataset: fields.ForeignKeyRelation[Dataset] = fields.ForeignKeyField('models.Dataset', related_name='related_models')

class Standard(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    value = fields.CharField(max_length=50)

class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

class Tag(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)

# 对于每一个dataset 记录filename（即image path）， tag对应的id，category对应的id，这两个可能是个list，以及dataset的id。
class DataInfo(Model):
    id = fields.IntField(pk=True)
    image_path = fields.CharField(max_length=255)
    dataset = fields.ForeignKeyField('models.Dataset', related_name='data_infos')
    categories = fields.ManyToManyField('models.Category', related_name='data_infos', through='image_category')
    tags = fields.ManyToManyField('models.Tag', related_name='data_infos', through='image_tag')
    results = fields.ReverseRelation['Result']
    question = fields.TextField()
    image_abs_path = fields.CharField(max_length=255, null="")

class Result(Model):
    id = fields.IntField(pk=True)
    dataset = fields.ForeignKeyField('models.Dataset', related_name='results')
    model = fields.ForeignKeyField('models.ModelName', related_name='results')
    data_info = fields.ForeignKeyField('models.DataInfo', related_name='results', to_field='id')
    answer = fields.TextField()
    score = fields.FloatField(null=True)
    standard = fields.FloatField(null=True)

# class DatasetInfo(BaseModel):
#     filename: str
#     question: str
#     tag: List[str] = Field(default_factory=list)
#     category: List[str] = Field(default_factory=list)




async def init_db():
    DATABASE_URL = "sqlite://db.sqlite3"
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["app.database"]})
    await Tortoise.generate_schemas()

async def model_run():
    # Initialize Tortoise-ORM and create the database tables
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["app.database"]})
    await Tortoise.generate_schemas()

    print("-----------------------------")

    # add dataset, model into table
    await add_datasets_from_directory('/mnt/afs/user/chenzixuan/eval_tool_info/results')

    #add standard
    await add_standards_from_json('/mnt/afs/user/chenzixuan/eval_tool_info/dataset')

    # add tag and category
    await process_josn_file('/mnt/afs/user/chenzixuan/eval_tool_info')

    # add result
    await process_results('/mnt/afs/user/chenzixuan/eval_tool_info/results')


async def add_datasets_from_directory(directory_path):
    """
    此函数从results目录中建dataset表和ModelName表
    """
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path,folder_name)
        if os.path.isdir(folder_path):
            # 检查这个 dataset 是否已存在
            dataset, created = await Dataset.get_or_create(name=folder_name)
            if created:
                print(f"Added dataset: {folder_name}")
            # 处理该数据集下的所有模型文件
            models_seen = set()
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.json') or file_name.endswith('.jsonl'):
                    model_name, _ = os.path.splitext(file_name)
                    if model_name not in models_seen:
                        models_seen.add(model_name)
                        if not await ModelName.filter(name=model_name,dataset=dataset).exists():
                            model_entry = ModelName(name=model_name, dataset=dataset)
                            await model_entry.save()

async def add_standards_from_json(directory_path):
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path,folder_name)
        json_path = os.path.join(folder_path,"json_files","standard.json")
        if os.path.exists(json_path):
            with open(json_path, 'r') as file:
                standards = json.load(file)
                if standards and isinstance(standards, list):
                    for standard_dict in standards[0].items():
                        name, value = standard_dict
                        if value == [0, 0.5, 1]:
                            value = 3
                        else:
                            value = 5
                        # elif value == "[0,1,2,3,4]":
                        #     value = 5
                        if not await Standard.filter(name=name).exists():
                            standard = Standard(name = name, value = value)
                            await standard.save()

async def process_josn_file(directory_path):
    """
    此函数从dataset目录中提取category tag和DataInfo生成表
    """
    tag_directory = os.path.join(directory_path, "dataset")
    for folder_name in os.listdir(tag_directory):
        folder_path = os.path.join(tag_directory, folder_name)
        if os.path.exists(folder_path):
            category_seen = set()
            tags_seen = set()
            json_file_path = os.path.join(folder_path,"json_files","dataset_info.json")
            dataset, _ = await Dataset.get_or_create(name=folder_name)  # 保证数据集存在
            if os.path.exists(json_file_path):
                with open(json_file_path, 'r') as json_file:
                    data_list = json.load(json_file)
                    for data in data_list:
                        filename = data["filename"]
                        if filename.startswith('images/'):
                            filename = filename[7:]  # 去掉前缀 'images/'
                        question = data["question"]
                        image_path = os.path.join(folder_path,"images",filename)
                        normalized_question = remove_end_point(question)
                        # create DataInfo item
                        try:
                            data_info, _ = await DataInfo.get_or_create(image_path=filename, dataset=dataset, question=normalized_question, image_abs_path=image_path)
                        except DoesNotExist as e:
                            raise e
                        # data_info, _ = await DataInfo.get_or_create(image_path=filename, dataset=dataset, question=question)
                        if data["category"]:
                            category_name = data["category"]
                            if category_name and category_name not in category_seen:
                                category_seen.add(category_name)
                                await Category.get_or_create(name=category_name)
                            # add category id into DataInfo
                            if category_name:
                                category, _ = await Category.get_or_create(name=category_name)
                                await data_info.categories.add(category)

                        if data["tag"]:
                            tags = data["tag"]
                            if tags and tags != "None":
                                tag_list = tags if isinstance(tags, list) else [tags]
                                for tag_name in tag_list:
                                    if tag_name not in tags_seen:
                                        tags_seen.add(tag_name)
                                        await Tag.get_or_create(name=tag_name)
                                # add tag id into DataInfo
                                for tag_name in tag_list:
                                    if tag_name:
                                        tag, _ = await Tag.get_or_create(name=tag_name)
                                        await data_info.tags.add(tag)  # 添加标签关联
                
async def process_results(directory_path):
    """
    此函数从results目录收集result来建表 利用DataInfo的数据进行关联
    """
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.exists(folder_path):
            dataset, _ = await Dataset.get_or_create(name=folder_name)  # 保证数据集存在
            for result_name in os.listdir(folder_path):
                if result_name.endswith('.json') or result_name.endswith('.jsonl'):
                    result_path = os.path.join(folder_path,result_name)
                    model_name, _ = os.path.splitext(result_name)
                    model,_ = await ModelName.get_or_create(name=model_name)

                    with open(result_path, 'r') as json_file:
                        # 这里json和jsonl格式可能是混乱的
                        try:
                            data_list = json.load(json_file)
                        except json.JSONDecodeError:
                            # 如果无法解析为 JSON，则将其视为 JSONL 文件
                            json_file.seek(0)
                            data_list = [json.loads(line) for line in json_file]
                        # data_list = json.load(json_file)
                        for data in data_list:
                            filename = data["filename"]
                            if '/' in filename:
                                filename = filename.split('/')[-1]
                            question = data["question"]
                            normalized_question = remove_end_point(question)
                            answer = data["result"]
                            # 首先根据 image_path 进行过滤
                            candidates = await DataInfo.filter(image_path=filename)
                            if len(candidates) == 1:
                                # 如果只有一个候选项，直接返回这个候选项
                                data_info =  candidates[0]
                            else:
                                # 如果image path不唯一，则再根据question来匹配
                                for candidate in candidates:
                                    if candidate.question == normalized_question:
                                        data_info = candidate
                                
                            
                            result = Result(dataset=dataset, model=model, data_info=data_info,answer=answer)
                            await result.save()

def get_image_as_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_iamge = base64.b64encode(file.read()).decode('utf-8')
    return encoded_iamge                

async def get_category_by_dataset(id: int):
    data_infos = await DataInfo.filter(dataset_id = id).prefetch_related('categories')
    category_set = set()
    for data_info in data_infos:
        category_set.update(data_info.categories)
    category_list = [{"id": category.id, "name": category.name} for category in category_set]

    return category_list

async def get_tags_by_dataset_and_categories(datasetID: int = None, categoryIDs: list = None):
    query = DataInfo.all().prefetch_related('tags')
    if datasetID is not None:
        query = query.filter(dataset_id=str(datasetID))
        count = await query.count()
    if categoryIDs:
        query = query.filter(categories__id__in=categoryIDs)
    data_infos = await query
    
    tags_set = set()
    for data_info in data_infos:
        tags = await data_info.tags.all()
        for tag in tags:
            tags_set.add(tag)
    
    tags_list = [{"id": tag.id, "name": tag.name} for tag in tags_set]
    return tags_list

def remove_end_point(msg: str):
    import unicodedata

    l = len(msg)
    idx = l - 1  # default value if all characters are punctuation
    while idx>=0 and unicodedata.category(msg[idx]) in {"Pd", "Ps", "Pe", "Pi", "Pf", "Po"}:
        idx -= 1
    return msg[: idx + 1]

async def get_filter_results(datasetID, modelIDs: list = None, TagIDs: list = None, categoryIDs: list = None, page: int = 1):
    datainfo_query = DataInfo.filter(dataset_id = datasetID)
    # Optional filters for tags and categories if lists are not empty
    if TagIDs:
        datainfo_query = datainfo_query.filter(tags__id__in=TagIDs)
    if categoryIDs:
        datainfo_query = datainfo_query.filter(categories__id__in=categoryIDs)

    total_count = await datainfo_query.count()
    print("total: ",total_count)
    
    page_size = 1 # 默认一页显示一条数据
    offset = (page - 1) * page_size
    print("offset", offset)
    datainfo_query = datainfo_query.offset(offset).limit(page_size)

    data_infos = await datainfo_query.prefetch_related('results').distinct()

    model_names = await ModelName.filter(id__in=modelIDs).values_list('id','name')
    model_id_to_name = {model_id: name for model_id, name in model_names}
    # Format the output
    pageInfo = []
    for data_info in data_infos:
        image_abs_path = data_info.image_abs_path
        mime_type = get_mime_type(image_abs_path)
        encoded_image = get_image_as_base64(image_abs_path)
        page_info = {
            "image_path": data_info.image_path,
            "question": data_info.question,
            "tags": [tag.name for tag in await data_info.tags],
            "categories": [category.name for category in await data_info.categories],
            "image_code": f"data:{mime_type};base64,{encoded_image}",
            "modelList": [
                {"model_id": result.model_id, 
                 "model_name": model_id_to_name.get(result.model_id, "Unknown Model"),
                 "answer": result.answer,
                 "score": result.score, 
                 "standard": result.standard}
                for result in await data_info.results.filter(model_id__in=modelIDs).only('model_id', 'answer','score', 'standard')
            ]
        }
        pageInfo.append(page_info)

    return {
        "total_page": total_count,
        "page_info": pageInfo[0]  # 前端默认只显示一页 故只传一条数据
    }

def get_mime_type(file_path):
    # 检查文件扩展名并确定 MIME 类型
    ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif'
    }
    mime_type = mime_types[ext]
    return mime_type

async def save_page_by_page(page, datasetID, modelID, score, standard, tagIDs: list = None, categoryIDs: list = None):
    datainfo_query = DataInfo.filter(dataset_id = datasetID)
    # Optional filters for tags and categories if lists are not empty
    if tagIDs:
        datainfo_query = datainfo_query.filter(tags__id__in=TagIDs)
    if categoryIDs:
        datainfo_query = datainfo_query.filter(categories__id__in=categoryIDs)
    total_count = await datainfo_query.count()
    print("total: ",total_count)
    page_size = 1 # 默认一页显示一条数据
    offset = (page - 1) * page_size
    print("offset", offset)
    datainfo_query = datainfo_query.offset(offset).limit(page_size)

    data_infos = await datainfo_query.prefetch_related('results').distinct()
    results = await Result.filter(data_info=data_infos[0].id, model_id=modelID).all()

    for result in results:
        print("===",1)
        result.score = score
        result.standard = standard
        await result.save()
        verify_result = await Result.get(id=result.id)
        if not (verify_result.score == score and verify_result.standard == standard):
            raise Exception("Verification failed, transaction will rollback")
        return "save successfully!"
