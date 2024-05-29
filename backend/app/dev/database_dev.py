from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from typing import Optional, List
from tortoise.query_utils import Prefetch
from tortoise.exceptions import DoesNotExist
from tortoise.functions import Count
from request_dev import ScoreFileRequest
import os
import json

import math


class Dataset(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    related_models = fields.ReverseRelation["ModelName"]

class ModelName(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
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
    answer = fields.TextField(null=True)
    score_3 = fields.FloatField(null=True, default=None)
    score_5 = fields.FloatField(null=True, default=None)
    score_else = fields.FloatField(null=True, default=None)
    standard = fields.FloatField(null=True)



async def init_db():
    DATABASE_URL = "sqlite://db.sqlite3"
    await Tortoise.init(db_url=DATABASE_URL, modules={"models": ["database_dev"]})
    await Tortoise.generate_schemas()

async def model_run():
    # Initialize Tortoise-ORM and create the database tables
    await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["database_dev"]})
    await Tortoise.generate_schemas()

    print("-----------------------------")

    # add dataset, model into table
    await add_datasets_from_directory('/mnt/afs/user/chenzixuan/eval_tool_info/dataset')

    #add standard
    await add_standards_from_json('/mnt/afs/user/chenzixuan/eval_tool_info/dataset')

    # add tag and category
    await process_josn_file('/mnt/afs/user/chenzixuan/eval_tool_info')

    # add result
    await process_results('/mnt/afs/user/chenzixuan/eval_tool_info/results')

    # add scored result
    await process_results_score('/mnt/afs/user/chenzixuan/eval_tool_info/results_score')


async def add_datasets_from_directory(dir):
    for folder_name in os.listdir(dir):
        if folder_name == "xiaomi_v1":
            continue
        folder_path = os.path.join(dir,folder_name)
        if os.path.isdir(folder_path):
            dataset, created = await Dataset.get_or_create(name=folder_name)
            if created:
                print(f"Added dataset: {folder_name}")


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
                        standard,_ = await Standard.get_or_create(name = name, value = value)

async def process_josn_file(directory_path):
    """
    此函数从dataset目录中提取category tag和DataInfo生成表
    """
    tag_directory = os.path.join(directory_path, "dataset")
    for folder_name in os.listdir(tag_directory):
        if folder_name == "xiaomi_v1":
            continue
        folder_path = os.path.join(tag_directory, folder_name)
        if os.path.exists(folder_path):
            try:
                dataset = await Dataset.get(name=folder_name)  # 保证数据集存在
                json_file_path = os.path.join(folder_path,"json_files","dataset_info.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        data_list = json.load(json_file)
                        for data in data_list:
                            await add_new_category_tag_datainfo(folder_path,data,dataset)
                        print(f"dataset, {folder_name},{len(data_list)}")
            except DoesNotExist:
                print(f"dataset {folder_name} not fount when process json file")
            

async def add_new_category_tag_datainfo(folder_path,data, dataset):
    filename = data["filename"]
    if filename.startswith('images/'):
        filename = filename[7:]  # 去掉前缀 'images/'
    question = data["question"]
    image_path = os.path.join(folder_path,"images",filename)
    normalized_question = remove_end_point(question)
    # create DataInfo item
    try:
        data_info, _ = await DataInfo.get_or_create(image_path=filename, dataset=dataset, question=normalized_question, image_abs_path=image_path)
        if "category" in data and data["category"]:
            category_name = data["category"]
            category, _ = await Category.get_or_create(name=category_name)
            # add category id into DataInfo
            await data_info.categories.add(category)

        if "tag" in data and data["tag"]:
                        tags = data["tag"]
                        if tags and tags != "None":
                            tag_list = tags if isinstance(tags, list) else [tags]
                            for tag_name in tag_list:
                                tag, _ = await Tag.get_or_create(name=tag_name)
                                await data_info.tags.add(tag)
    except DoesNotExist as e:
        raise e
    


async def update_datainfo_category_tag(folder_path,dataset):
    json_file_path = os.path.join(folder_path,"json_files","dataset_info.json")
    if os.path.exists(json_file_path):
        # 获取dataset下的所有DataInfo
        data_infos = await DataInfo.filter(dataset=dataset).order_by('id')
        print("已找到的datainfo个数",len(data_infos))
        with open(json_file_path, 'r') as json_file:
            data_list = json.load(json_file)
            for index, data in enumerate(data_list):

                if index < len(data_infos):
                    data_info = data_infos[index]
                    await update_datainfo(folder_path, data_info, data,dataset)
                else:
                    # 如果data_list比现有的DataInfo更多，则创建新的DataInfo
                    await add_new_category_tag_datainfo(folder_path,data,dataset)

async def update_datainfo(folder_path, data_info, data,dataset):
    filename = data["filename"]
    if filename.startswith('images/'):
        filename = filename[7:]  # 去掉前缀 'images/'
    question = data["question"]
    image_path = os.path.join(folder_path,"images",filename)
    normalized_question = remove_end_point(question)

    update_needed = False
    if data_info.image_path != filename:
        data_info.image_path = filename
        update_needed = True
    if data_info.image_abs_path != image_path:
        data_info.image_abs_path = image_path
        update_needed = True
    if data_info.question != normalized_question:
        data_info.question = normalized_question
        update_needed = True
    
    
    # 更新新的 categories 和 tags
    if "category" in data and data["category"]:
        # 删除旧的 categories 和 tags
        await data_info.categories.clear()
        category_name = data["category"]
        category, _ = await Category.get_or_create(name=category_name)
        # add category id into DataInfo
        await data_info.categories.add(category)

    if "tag" in data and data["tag"]:
        tags = data["tag"]
        if tags and tags != "None":
            await data_info.tags.clear()
            tag_list = tags if isinstance(tags, list) else [tags]
            for tag_name in tag_list:
                tag, _ = await Tag.get_or_create(name=tag_name)
                await data_info.tags.add(tag)

    if update_needed:
        await data_info.save()
        print(f"DataInfo {data_info.id} updated.")
    

async def process_results(directory_path):
    """
    此函数从results目录收集result来建表 利用DataInfo的数据进行关联
    """
    for folder_name in os.listdir(directory_path):
        # 这里的folder name是dataset
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.exists(folder_path):
            try:
                dataset = await Dataset.get(name=folder_name)  # 保证数据集存在
                for result_name in os.listdir(folder_path):
                    result_path = os.path.join(folder_path,result_name)
                    await add_result(dataset,result_name,result_path)
            except DoesNotExist:
                print(f"Dataset {folder_name} does not exist in results_score")
                pass
           

async def add_result(dataset, result_name, result_path):
    # folder_path, folder_name
    if result_name.endswith('.json') or result_name.endswith('.jsonl'):
        model_name, _ = os.path.splitext(result_name)
        try:
            model,_ = await ModelName.get_or_create(name=model_name, dataset=dataset)
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
                    if filename.startswith('images/'):
                        filename = filename[7:]  # 去掉前缀 'images/'
                    question = data.get("question") or data.get("ask_question")
                    normalized_question = remove_end_point(question)
                    answer = data["result"]
                    # 首先根据 image_path 进行过滤
                    candidates = await DataInfo.filter(image_path=filename)
                    data_info = None
                    if len(candidates) == 1:
                        # 如果只有一个候选项，直接返回这个候选项
                        data_info =  candidates[0]
                    else:
                        # 如果image path不唯一，则再根据question来匹配
                        for candidate in candidates:
                            if candidate.question == normalized_question:
                                data_info = candidate
                                break
                    assert data_info, "Error, data_info not found"
                    print(f"add result, model {model_name}, data_info {data_info.id}")
                    result,_ = await Result.get_or_create(dataset=dataset, model=model, data_info=data_info,answer=answer)
        
        except DoesNotExist:
                pass


async def process_results_score(directory_path):
    """
    此函数从results_score目录收集score加进Result这个model里 利用DataInfo的数据进行关联
    """
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        if os.path.exists(folder_path):
            try:
                dataset = await Dataset.get(name=folder_name) 
                for model_name in os.listdir(folder_path):
                    model_path = os.path.join(folder_path, model_name)
                    await add_score(dataset,model_name,model_path)
            except DoesNotExist:
                print(f"Dataset {folder_name} does not exist in results_score")
                pass


async def add_score(dataset, model_name, model_path):
    if model_name.endswith('.json') or model_name.endswith('.jsonl'):
        standard = None
        if 'xiaomi_standard' in model_name:
            standard = 3
        elif '_intern_standard' in model_name:
            standard = 5
        # 去掉从第一个横杠开始的部分及文件后缀
        # model_name = re.sub(r'-.*$', '', model_name)
        model_name = model_name.replace('-xiaomi_standard','').replace('-intern_standard','').replace('.json','').replace('.jsonl','')

        try:
            model = await ModelName.get(name=model_name,dataset=dataset)
            with open(model_path, 'r') as json_file:
                data_list = json.load(json_file)
                
                for data in data_list:
                    filename = data["filename"]
                    # if '/' in filename:
                    #     filename = filename.split('/')[-1]
                    question = data.get("question") or data.get("ask_question")
                    normalized_question = remove_end_point(question)
                    score = data.get("score")
                    print(f"score : {score}, {model_name}")
                    if score is None or isinstance(score, float) and math.isnan(score):
                        continue
                    # 首先根据 image_path 进行过滤
                    candidates = await DataInfo.filter(image_path=filename)
                    data_info = None
                    if len(candidates) == 1:
                        data_info =  candidates[0]
                    else:
                        # 如果image path不唯一，则再根据question来匹配
                        for candidate in candidates:
                            if candidate.question == normalized_question:
                                data_info = candidate
                    assert data_info, f"Error, data_info not found, {filename}, {question}"
                    try:
                        result_count = await Result.filter(dataset=dataset,model=model,data_info = data_info).count()
                        result = await Result.get(dataset=dataset,model=model,data_info = data_info)
                        try:
                            score = float(score)
                        except ValueError:
                            # Handle the case where conversion fails if necessary
                            print(f"Invalid score value: {score}")
                            score = 0.0
                        if(standard == 3):
                            result.score_3 = score
                        elif standard==5:
                            result.score_5 = score
                        else:
                            result.score_else = score
                        result.standard = standard
                        await result.save()
                        
                    except DoesNotExist:
                        # 如果 Result 不存在，处理异常情况
                        print(f"Result with model={model_name}, data_info={data_info.image_path} does not exist")
                        pass
            
        except DoesNotExist:
            print(f"model={model_name} does not exist")
            pass
                

def remove_end_point(msg: str):
    import unicodedata

    l = len(msg)
    idx = l - 1  # default value if all characters are punctuation
    while idx>=0 and unicodedata.category(msg[idx]) in {"Pd", "Ps", "Pe", "Pi", "Pf", "Po"}:
        idx -= 1
    return msg[: idx + 1]

# async def add_file(datasetID,):

