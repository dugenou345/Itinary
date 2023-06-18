from bson import ObjectId
from my_projection import pipeline
import json
from decorators import progress_bar

#function to export selected data to json from mongodb
@progress_bar
def export_filtered_data_json(client,database,collection):
    database = client[database]
    collection = database[collection]

    # search for mongodb and extract result based on my_projection
    result = collection.aggregate(pipeline)
    # Convert the result to a list of dictionaries
    documents = list(result)
    # Define the file path for exporting the JSON data
    file_path = "data_result/result_filtered.json"

    # Write the documents to the JSON file using the custom encoder
    # Iterate over the result
    with open(file_path, "w") as file:
        for doc in documents:
            json.dump(doc, file, cls=MongoEncoder)
            file.write("\n")

# Custom JSON encoder to handle MongoDB ObjectId
class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)