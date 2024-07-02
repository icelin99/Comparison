from database_dev import Result, DataInfo, Tag, ModelName, Dataset, Category, Standard,  add_result, add_score, update_datainfo_category_tag, add_new_category_tag_datainfo, del_dataset_result
from request_dev import SaveRequest, ScoreFileRequest
from database_dev import remove_end_point
from tortoise.exceptions import DoesNotExist
from fastapi.responses import JSONResponse, StreamingResponse
from typing import List
import base64
import os
import json
from io import BytesIO
# from tortoise.query_utils import Q


def get_image_as_base64(file_path):
    with open(file_path, 'rb') as file:
        encoded_iamge = base64.b64encode(file.read()).decode('utf-8')
    return encoded_iamge                

async def get_categories(dataset_id: int, model_ids: list, tag_ids: list = []):
    # 获取符合 dataset_id 和 model_ids 条件的 data_info_id 列表
    data_info_ids = await Result.filter(
        dataset_id=dataset_id,
        model_id__in=model_ids
    ).distinct().values_list('data_info_id', flat=True)
    if tag_ids:
        data_info_ids_with_tags = await DataInfo.filter(
            id__in=data_info_ids,
            tags__id__in=tag_ids
        ).distinct().values_list('id', flat=True)
        categories = await Category.filter(
            data_infos__id__in=data_info_ids_with_tags
        ).distinct().values('id', 'name')
    else:
        categories = await Category.filter(
            data_infos__id__in=data_info_ids
        ).distinct().values('id', 'name')
    return list(categories)

async def get_tags(dataset_id: int, model_ids: list, category_ids: list = []):
    # 获取符合 dataset_id 和 model_ids 条件的 data_info_id 列表
    data_info_ids = await Result.filter(
        dataset_id=dataset_id,
        model_id__in=model_ids
    ).distinct().values_list('data_info_id', flat=True)
    if category_ids:
        # 如果 category_ids 不为空，根据 category 筛选 data_info_id
        data_info_ids_with_categories = await DataInfo.filter(
            id__in=data_info_ids,
            categories__id__in=category_ids
        ).distinct().values_list('id', flat=True)
        
        # 根据筛选出的 data_info_id 获取 tags
        tags = await Tag.filter(
            data_infos__id__in=data_info_ids_with_categories
        ).distinct().values('id', 'name')
    else:
        # 如果 category_ids 为空，直接根据 data_info_id 获取 tags
        tags = await Tag.filter(
            data_infos__id__in=data_info_ids
        ).distinct().values('id', 'name')
    
    return list(tags)

async def get_category_by_dataset(datasetID: int, modelIDs= List[int]):
    # 从Result表中找到对应的data_info_id
    data_info_ids = await Result.filter(dataset_id=datasetID, model_id__in=modelIDs)
    # 使用这些data_info_id从DataInfo表中获取对应的Category
    data_infos = await DataInfo.filter(id__in = data_info_ids).prefetch_related('categories')
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


async def get_filter_results(datasetID, modelIDs: list , standard: int, TagIDs: list = None, categoryIDs: list = None, page: int = 1):
    print(datasetID,modelIDs,standard,TagIDs,categoryIDs,page)
    pageInfo = []
    first_data_info = None
    first_model_id = modelIDs[0]
    result_query = Result.filter(dataset_id=datasetID, model_id=first_model_id)
    if TagIDs:
        result_query = result_query.filter(data_info__tags__id__in=TagIDs)
    if categoryIDs:
        result_query = result_query.filter(data_info__categories__id__in=categoryIDs)
    total_count = await result_query.count()
    print("total: ", total_count)
    # debug #################
    result_query_all = result_query.order_by('data_info__id')
    all_results = await result_query_all.distinct()
    result_ids = [result.id for result in all_results]
    data_info_ids = [result.data_info_id for result in all_results]
    print("All data_info ids:", data_info_ids)
    #########################
    page_size = 1  # 默认一页显示一条数据
    offset = (page - 1) * page_size
    result_query = result_query.order_by('data_info__id').offset(offset).limit(page_size)
    first_result = await result_query.distinct()
    if first_result:
        first_data_info = first_result[0].data_info_id
    print("first data into id",first_data_info)

    page_info = {
        "image_path": None,
        "question": None,
        "ref_answer": None,
        "tags": [],
        "categories": [],
        "image_code": None,
        "data_info_id": first_data_info,
        "modelList": []
    }

    for modelID in modelIDs:
        result_query = Result.filter(dataset_id=datasetID,model_id=modelID, data_info_id = first_data_info)

        results = await result_query.distinct()

        model_names = await ModelName.filter(id=modelID).values_list('id', 'name')
        model_id_to_name = {model_id: name for model_id, name in model_names}
        for result in results:
            data_info = await result.data_info
            image_abs_path = data_info.image_abs_path
            mime_type = get_mime_type(image_abs_path)
            encoded_image = get_image_as_base64(image_abs_path)
            score = None
            if standard == 3:
                score = result.score_3
            elif standard == 5:
                score = result.score_5
            else: 
                score = result.score_10
            
            if not page_info["image_path"]:
                page_info.update({
                    "image_path": data_info.image_path,
                    "question": data_info.question,
                    "ref_answer": data_info.ref_answer,
                    "tags": [tag.name for tag in await data_info.tags],
                    "categories": [category.name for category in await data_info.categories],
                    "image_code": f"data:{mime_type};base64,{encoded_image}",
                    "data_info_id": first_data_info
                })

            model_entry = {
                "model_id": result.model_id,
                "model_name": model_id_to_name.get(result.model_id, "Unknown Model"),
                "answer": result.answer,
                "score": score,
                "standard": result.standard
            }

            if result.standard in [5, 10]:
                model_entry["reason"] = result.reason

            page_info["modelList"].append(model_entry)

    return {
        "total_page": total_count,
        "page_info": page_info  # 前端默认只显示一页 故只传一条数据
    }



def get_mime_type(file_path):
    # 检查文件扩展名并确定 MIME 类型
    ext = os.path.splitext(file_path)[1].lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types[ext]
    return mime_type

async def save_page_by_page(page, data_info_id,datasetID, modelID, standard, score: float = None):
    result_query = Result.filter(dataset_id=datasetID,model_id=modelID,data_info_id=data_info_id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!")
    

    results = await result_query.distinct()
    for result in results:
        print("=======",1)
        if standard == 3:
            result.score_3 = score
        elif standard ==5:
            result.score_5 = score
        else:
            result.score_10 = score
        result.standard = standard
        await result.save()
        # verify_result = await Result.get(id=result.id)
        # if not (verify_result.score == score and verify_result.standard == standard):
        #     raise Exception("Verification failed, transaction will rollback")
        return "save successfully!"
    return "save failed"


async def read_file(file,filetype):
    """
    这个函数处理从前端传来的文件
    """
    filename = file.filename
    file_extension = filename.split('.')[-1]
    print('--',filetype)
    try:
        file_data = await file.read()
        file_content = file_data.decode('utf-8')
        if file_extension == 'json':
            json_data = json.loads(file_content)
            if isinstance(json_data, list):
                score_file_requests = [ScoreFileRequest(**item) for item in json_data]
                await update_db_by_data(score_file_requests, filename)
                return {"filename": file.filename, "message": "upload successfully", "details": [request.dict() for request in score_file_requests]}
            else:
                score_file_request = ScoreFileRequest(**json_data)
                await update_db_by_data(score_file_request, filename)
                return {"filename": file.filename, "message": "upload successfully", "details": score_file_request.dict()}
        
        elif file_extension == 'jsonl':
            print("jsonl")
            lines = file_content.splitlines()
            score_file_requests = []
            for line in lines:
                try:
                    json_data = json.loads(line)
                    score_file_request = ScoreFileRequest(**json_data)
                    score_file_requests.append(score_file_request)
                    await update_db_by_data(score_file_requests, filename)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error for line: {line} - {e}")
                    raise e
            return {"filename": file.filename, "message": "upload successfully"}
    except Exception as e:
        print("fail to read file")
        return {"error": f"Failed to process file: {str(e)}"}
    
async def update_db_by_data(data: List[ScoreFileRequest],result_name):
    print("enter the udpate func")
    for item in data:
        print(item)
        filename = item.filename
        question = item.question
        normalized_question = remove_end_point(question)
        try:
            data_info = await DataInfo.get(image_path = filename, question=normalized_question)
            dataset = await Dataset.get(id=data_info.dataset_id)
            model_name = result_name.rpartition('.')[0]
            print(data_info.id,data_info.dataset_id,model_name)
            model,_ = await ModelName.get_or_create(name=model_name,dataset=dataset)
            print("mode id",model.id)
            if item.category:
                category_name = data.category
                category,_ = await Category.get_or_create(name=category_name)
                await data_info.categories.add(category)
            if item.tag:
                tags = item.tag
                tag_list = tags if isinstance(tags, list) else [tags]
                for tag_name in tag_list:
                    tag,_ = await Tag.get_or_create(name=tag_name)
                    await data_info.tags.add(tag)
            try:
                result = Result.get(data_info=data_info,dataset_id=data_info.dataset_id,model=model)
                result.score=item.score
                await result.save()
                print("修改score")
            except DoesNotExist:
                result,_ = Result.get_or_create(data_info=data_info.id,dataset_id=data_info.dataset_id,model=model,answer=data.result)
                print("新建result")
        except DoesNotExist:
            print("filename and question does not exist!!")
            pass    

async def update_dataset_by_path(dataset_dir):
    # 检查地址是否存在
    if os.path.exists(dataset_dir):
        # 提取dataset
        dir_name = os.path.basename(os.path.normpath(dataset_dir))
        print("dataset dir", dir_name)
        check_file = check_dataset_info(dataset_dir)
        if check_file == "OK":
            try:
                dataset = await Dataset.get(name=dir_name)
                try:
                    await update_datainfo_category_tag(dataset_dir,dir_name,dataset)
                    return {"success": "成功更新dataset和datainfo！"}
                except Exception as e:
                    del_dataset(dir_name)
                    return {"error": str(e)}
            except DoesNotExist:
                print("data set 新增")
                dataset = await Dataset.create(name=dir_name)
                json_file_path = os.path.join(dataset_dir,"json_files","dataset_info.json")
                if os.path.exists(json_file_path):
                    with open(json_file_path, 'r') as json_file:
                        data_list = json.load(json_file)
                        for data in data_list:
                            await add_new_category_tag_datainfo(dataset_dir,data,dataset)
                    return {"success": "成功新建dataset和datainfo！"}
        else:
            return {"error": check_file}
       
    else:
        return {"error": "路径不存在"}

async def update_result_by_path(result_path):
    # 检查地址是否存在
    if os.path.exists(result_path):
        file_name = os.path.basename(result_path)
        dataset_name = os.path.basename(os.path.dirname(result_path))
        dataset_dir = os.path.join('/mnt/afs/user/chenzixuan/eval_tool_info/dataset',dataset_name)
        check = check_result_file(dataset_dir,result_path)
        print("filename",file_name, "dataset_name", dataset_name,"check",check)
        if check == "OK":
            try:
                dataset = await Dataset.get(name=dataset_name)
                try:
                    await add_result(dataset, file_name,result_path)
                    return {"success": "添加result结果成功！"}
                except Exception as e:
                    return {"error": str(e)}
            except DoesNotExist:
                return {"error": "dataset 不存在"}
        else:
            return {"error": check}
    else:
        return {"error": "路径不存在"}

async def update_score_by_path(score_path):
    # 检查地址是否存在
    if os.path.exists(score_path):
        file_name = os.path.basename(score_path)
        dataset_name = os.path.basename(os.path.dirname(score_path))
        dataset_dir = os.path.join('/mnt/afs/user/chenzixuan/eval_tool_info/dataset',dataset_name)
        check = check_score_file(dataset_dir,score_path,file_name,dataset_name)
        print("dataset ",dataset_name, " file name ", file_name)
        if check == "OK":
            model_name = file_name.replace('-xiaomi_standard','').replace('-gpt4_ten_point','').replace('-gpt4_five_point','').replace('.jsonl','').replace('.json','')
            try:
                dataset = await Dataset.get(name=dataset_name)
                try:
                    model = await ModelName.get(name=model_name,dataset=dataset)
                    try:
                        await add_score(dataset, file_name,score_path)
                        return {"success": "添加score结果成功！"}
                    except Exception as e:
                        return {"error": e} 
                except DoesNotExist:
                    return {"error": "model未被定义"}
            except DoesNotExist:
                return {"error": "dataset 不存在"}
        else:
            return {"error": check}
        
    else:
        return {"error": "路径不存在"}

async def fetch_save_file(datasetID, modelID,standard):

    dataset = await Dataset.get(id=datasetID)
    model = await ModelName.get(id=modelID)
    standard_model = await Standard.filter(value=standard).first()
    results = await Result.filter(
            dataset_id=datasetID,
            model_id=modelID,
            standard=standard
        ).prefetch_related('data_info', 'data_info__categories')
    results_length = await Result.filter(
        dataset_id=datasetID,
        model_id=modelID,
        standard=standard
    ).count()
    if not results:
        return "empty"
    data = []
    print("result 长度",results_length)
    for result in results:
        categories = [category.name for category in await result.data_info.categories.all()]
        entry = {
            "filename": result.data_info.image_path,
            "question": result.data_info.question,
            "category": ", ".join(categories),
            "ref_answer": result.data_info.ref_answer,
            "answer": result.answer,
            "reason": result.reason,
            "score": result.score_3 if standard == 3 else result.score_5 if standard == 5 else result.score_10
        }
        data.append(entry)
    
    file_name = f"results_{dataset.name}_{model.name}_{standard_model.name}.json"
    file_content = json.dumps(data, ensure_ascii=False).encode('utf-8')
   
    return JSONResponse(content={"file_content": file_content.decode('utf-8'), "file_name": file_name})

async def fetch_save_dataset(datasetID):
    dataset = await Dataset.get(id=datasetID)
    data_infos = await DataInfo.filter(dataset_id = datasetID).prefetch_related('categories', 'tags').values(
        'image_path', 'categories__name', 'tags__name', 'question', 'ref_answer'
    )
    dataset_info = []
    for item in data_infos:
        print("categories",item)
        entry = {
            "image_path": item['image_path'],
            "question": item['question'],
            "ref_answer": item['ref_answer'],
            "tag": item['categories__name'],
            "category": item['tags__name']
        }
        dataset_info.append(entry)
    
    file_name = f"{dataset.name}_dataset_info.json"
    file_content = json.dumps(dataset_info, ensure_ascii=False).encode('utf-8')
    return JSONResponse(content={"file_content": file_content.decode('utf-8'), "file_name": file_name})
   



def check_dataset_info(dataset_dir):
    required_keys = {'filename', 'question', 'category', 'tag'}
    base_image_path = os.path.join(dataset_dir,'images')
    file_path = os.path.join(dataset_dir,"json_files","dataset_info.json")
    try:
        with open(file_path,'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("文件不是有效的JSON格式")
        return "文件不是有效的JSON格式"
    
    # 检查是否是一个列表
    if not isinstance(data, list):
        print("文件内容应为一个列表")
        return "文件内容应为一个列表"
    
    # 检查每一项是否包含所需的键并且filename路径存在
    for item in data:
        if not all(key in item for key in required_keys):
            print(f"项缺少所需的键: {item}")
            return "缺少所需的键"
        if not os.path.exists(os.path.join(base_image_path, item['filename'])):
            print(f"文件路径不存在: {os.path.join(base_image_path, item['filename'])}")
            return "文件路径不存在"

    return "OK"

def check_result_file(dataset_dir,file_path):
    required_keys = {'filename', 'question', 'result'}
    base_image_path = os.path.join(dataset_dir,'images')
    data = []
    # 检查文件是否为 JSON 或 JSONL 格式
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline().strip()
            if first_line.startswith('['):  # JSON 格式
                file.seek(0)  # 回到文件开头
                data = json.load(file)
            else:  # JSONL 格式
                file.seek(0)  # 回到文件开头
                data = [json.loads(line.strip()) for line in file]
    except json.JSONDecodeError:
        print("文件不是有效的 JSON 或 JSONL 格式")
        return "文件不是有效的 JSON 或 JSONL 格式"
    # 检查是否是一个列表
    if not isinstance(data, list):
        print("文件内容应为一个列表")
        return "文件内容应为一个列表"
    # 检查每一项是否包含所需的键并且 filename 路径存在
    for item in data:
        if not all(key in item for key in required_keys):
            print(f"项缺少所需的键: {item}")
            return "缺少所需的键"
        if not os.path.exists(os.path.join(base_image_path, item['filename'])):
            print(f"文件路径不存在: {os.path.join(base_image_path, item['filename'])}")
            return "文件路径不存在"

    return "OK"

def check_score_file(dataset_dir,score_path,score_name,dataset_name):
    required_keys = {'filename', 'question', 'score'}
    base_image_path = os.path.join(dataset_dir,'images')
    data = []
    # 检查文件是否为 JSON 或 JSONL 格式
    try:
        with open(score_path, 'r') as file:
            first_line = file.readline().strip()
            if first_line.startswith('['):  # JSON 格式
                file.seek(0)  # 回到文件开头
                data = json.load(file)
            else:  # JSONL 格式
                file.seek(0)  # 回到文件开头
                data = [json.loads(line.strip()) for line in file]
    except json.JSONDecodeError:
        print("文件不是有效的 JSON 或 JSONL 格式")
        return "文件不是有效的 JSON 或 JSONL 格式"
    # 检查是否是一个列表
    if not isinstance(data, list):
        print("文件内容应为一个列表")
        return "文件内容应为一个列表"
    # 检查每一项是否包含所需的键并且 filename 路径存在
    for item in data:
        if not all(key in item for key in required_keys):
            print(f"项缺少所需的键: {item}")
            return "缺少所需的键"
        if not os.path.exists(os.path.join(base_image_path, item['filename'])):
            print(f"文件路径不存在: {os.path.join(base_image_path, item['filename'])}")
            return "文件路径不存在"

    # 检查 score filename 是否在 result 中有对应的文件名
    # if check_filename_in_directory(score_name,dataset_name) == False:
    #     return "在result中没有对应的模型名"
    return "OK"

def check_filename_in_directory(filename,dataset_name):
    stripped_filename = filename.replace('-xiaomi_standard','').replace('-gpt4_ten_point','').replace('-gpt4_five_point','').replace('.jsonl','').replace('.json','')
    print("check name", stripped_filename)
    for result_name in os.listdir(os.path.join('/mnt/afs/user/chenzixuan/eval_tool_info/results',dataset_name)):
        result_name_check = result_name.replace('.jsonl','').replace('.json','')
        if result_name_check == stripped_filename:
            return True
    return False

async def save_ref_answer(data_info_id, ref_answer):
    data_info = await DataInfo.get(id=data_info_id)
    print("save ref answer:",data_info_id,)
    if data_info:
        data_info.ref_answer = ref_answer
        await data_info.save()
    else:
        return {"error": "DataInfo not found"}

    return {"success": "Ref answer saved successfully"}


async def get_accuracy_table(datasetIDs, modelIDs, standard):
    # 目前只允许一个dataset
    if isinstance(datasetIDs,(int, float)):
        datasetIDs = [datasetIDs]
    accuracy_table = {}
    model_names = await ModelName.filter(id__in=modelIDs).values_list('id', 'name')
    model_id_to_name = {model_id: name for model_id, name in model_names}
    for dataset_id in datasetIDs:
        data_infos = await DataInfo.filter(dataset_id=dataset_id).prefetch_related('categories', 'tags', 'results')
        categories = {}
        for data_info in data_infos:
            if data_info.categories:
                for category in data_info.categories:
                    if category.id not in categories:
                        categories[category.id] = {'name': category.name, 'tags': {}}
                    if data_info.tags:
                        for tag in data_info.tags:
                            if tag.id not in categories[category.id]['tags']:
                                categories[category.id]['tags'][tag.id] = {'name': tag.name, 'data_infos': []}
                            categories[category.id]['tags'][tag.id]['data_infos'].append(data_info.id)
                    else:
                        if 'None' not in categories[category.id]['tags']:
                            categories[category.id]['tags']['None'] = {'name': 'None', 'data_infos': []}
                        categories[category.id]['tags']['None']['data_infos'].append(data_info.id)
            else:
                if 'None' not in categories:
                    categories['None'] = {'name': 'None', 'tags': {}}
                if data_info.tags:
                    for tag in data_info.tags:
                        if tag.id not in categories['None']['tags']:
                            categories['None']['tags'][tag.id] = {'name': tag.name, 'data_infos': []}
                        categories['None']['tags'][tag.id]['data_infos'].append(data_info.id)
                else:
                    if 'None' not in categories['None']['tags']:
                        categories['None']['tags']['None'] = {'name': 'None', 'data_infos': []}
                    categories['None']['tags']['None']['data_infos'].append(data_info.id)
        print("dataset id",dataset_id, " category",categories)
        for category_id, category_data in categories.items():
            for tag_id, tag_data in category_data['tags'].items():
                model_scores = {model_id: [] for model_id in modelIDs}
                data_info_count = len(tag_data['data_infos'])
                for data_info in tag_data['data_infos']:
                    results = await Result.filter(dataset_id=dataset_id, data_info_id=data_info, model_id__in=modelIDs)
                    for result in results:
                        score = None
                        if int(standard) == 3:
                            score = result.score_3
                        if int(standard) == 5:
                            score = result.score_5
                        if int(standard == 10):
                            score = result.score_10
                        if score is not None:
                            model_scores[result.model_id].append(score)
                        

                for model_id, scores in model_scores.items():
                    if scores:
                        accuracy = sum(scores) / len(scores) * 100
                        if int(standard) == 5:
                            accuracy = accuracy / 4
                    else:
                        accuracy = None
                    dataset__ = await Dataset.get(id=dataset_id)
                    if dataset__.name not in accuracy_table:
                        accuracy_table[dataset__.name] = {}
                    if category_data["name"] not in accuracy_table[dataset__.name]:
                        accuracy_table[dataset__.name][category_data["name"]] = {}
                    if tag_data["name"] not in accuracy_table[dataset__.name][category_data["name"]]:
                        accuracy_table[dataset__.name][category_data["name"]][tag_data["name"]] = {
                            "count": data_info_count,
                            "models": [],
                        }
                    accuracy_table[dataset__.name][category_data["name"]][tag_data["name"]]["models"].append({
                        'model_id': model_id,
                        'model_name': model_id_to_name.get(model_id),
                        'accuracy': "None" if accuracy is None else "%.2f%%" % accuracy
                    })
    print(accuracy_table)
    return accuracy_table    



async def del_dataset(dataset_name):
    print(dataset_name)
    try:
        dataset = await Dataset.get(name=dataset_name)
        print(dataset.id)
        await del_dataset_result(dataset)
        await Dataset.filter(name=dataset_name).delete()
        return {"success": "成功删除dataset和对应的所有result！"}

    except DoesNotExist:
        return {"error":"dataset不存在"}

async def del_result(result_path):
    if os.path.exists(result_path):
        file_name = os.path.basename(result_path)
        dataset_name = os.path.basename(os.path.dirname(result_path))
        model_name = file_name.replace(".jsonl","").replace(".json","")
        try:
            dataset = await Dataset.get(name=dataset_name)
            try:
                model = await ModelName.get(name=model_name, dataset_id = dataset.id)
                try:
                    await Result.filter(dataset=dataset, model=model).delete()
                    await ModelName.filter(dataset=dataset, name=model_name).delete()
                    return {"success": "删除result结果成功！"}
                except Exception as e:
                    return {"error": e}
            except DoesNotExist:
                return {"error": "model 不存在"}
        except DoesNotExist:
            return {"error": "dataset 不存在"}
        
async def change_modelname(datasetID, modelID, modelname):
    try:
        dataset = await Dataset.get(id=datasetID)
        try:
            model = await ModelName.get(dataset = dataset, id=modelID)
            try:
                model.name = modelname
                await model.save()
                return {"success": "更改模型名称成功"}
            except DoesNotExist:
                return {"error": "更改模型名称失败"}
        except DoesNotExist:
            return {"error": "model 不存在"}
    except DoesNotExist:
        return {"error": "dataset 不存在"}
