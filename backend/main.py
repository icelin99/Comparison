# from tortoise import Tortoise, fields, run_async
# from tortoise.models import Model
# from tortoise.query_utils import Prefetch


# class Dataset(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=50, unique=True)
#     data_infos: fields.ReverseRelation["DataInfo"]


# class DataInfo(Model):
#     id = fields.IntField(pk=True)
#     dataset: fields.ForeignKeyRelation[Dataset] = fields.ForeignKeyField(
#         "models.Dataset", related_name="data_infos"
#     )
#     image_data = (
#         fields.TextField()
#     )  # This should be a BinaryField or similar, depending on your actual requirements
#     question = fields.TextField()
#     tags: fields.ManyToManyRelation["Tag"] = fields.ManyToManyField(
#         "models.Tag", related_name="data_infos"
#     )
#     categories: fields.ManyToManyRelation["Category"] = fields.ManyToManyField(
#         "models.Category", related_name="data_infos"
#     )


# class Tag(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=50, unique=True)
#     data_infos: fields.ManyToManyRelation[DataInfo]


# class Category(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=50, unique=True)
#     data_infos: fields.ManyToManyRelation[DataInfo]


# class Model(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=50, unique=True)
#     results: fields.ReverseRelation["Result"]


# class Result(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=100, unique=True)
#     model: fields.ForeignKeyRelation[Model] = fields.ForeignKeyField(
#         "models.Model", related_name="results"
#     )
#     data_info: fields.ForeignKeyRelation[DataInfo] = fields.ForeignKeyField(
#         "models.DataInfo", related_name="results"
#     )
#     answer = fields.TextField()
#     score = fields.FloatField()
#     standard = fields.FloatField()


# async def run():
#     # Initialize Tortoise-ORM and create the database tables
#     await Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["__main__"]})
#     await Tortoise.generate_schemas()

#     # Create a new dataset
#     dataset = await Dataset.create(name="Dataset 1")

#     # Create some new data info
#     data_info1 = await DataInfo.create(
#         dataset=dataset, image_data="Image data 1", question="Question 1"
#     )
#     data_info2 = await DataInfo.create(
#         dataset=dataset, image_data="Image data 2", question="Question 2"
#     )

#     # Create some new tags and categories
#     tag1 = await Tag.create(name="Tag 1")
#     tag2 = await Tag.create(name="Tag 2")
#     category1 = await Category.create(name="Category 1")
#     category2 = await Category.create(name="Category 2")

#     # Add the tags and categories to the data info
#     await data_info1.tags.add(tag1, tag2)
#     await data_info1.categories.add(category1, category2)

#     # Create a new model
#     model = await Model.create(name="Model 1")

#     # Create some new results
#     result1 = await Result.create(
#         name="Result 1", model=model, data_info=data_info1, answer="Answer 1", score=0.9
#     )
#     result2 = await Result.create(
#         name="Result 2", model=model, data_info=data_info2, answer="Answer 2", score=0.8
#     )

#     # Fetch some data from the database
#     datasets = await Dataset.all().prefetch_related("data_infos")
#     for dataset in datasets:
#         print(dataset.name)
#         for data_info in dataset.data_infos:
#             print(data_info.image_data, data_info.question)
#             await data_info.fetch_related("tags", "categories")
#             for tag in data_info.tags:
#                 print(tag.name)
#             for category in data_info.categories:
#                 print(category.name)


# if __name__ == "__main__":
#     run_async(run())
