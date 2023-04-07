from pymongo import MongoClient, DESCENDING

class mongo_dba:
    def __init__(self, collection):

        self.host = 'localhost'
        self.port = 27017
        self.con = MongoClient(self.host, self.port)
        self.db = self.con.plantsense
        
        if collection == "sensor_values":
            self.col = self.db.sensor_values
        if collection == "plant_data":
            self.col = self.db.plant_data
        if collection == "watering_system":
            self.col = self.db.watering_system

    def get_last_sensor_values(self):
        output = self.col.find_one(sort=[( '_id', DESCENDING )])
        if output:
            res = output
            print(res)
            res['_id'] = str(res['_id'])
            return res
        else:
            return None

    def post_data(self, data):
        self.col.insert_one(data)

    def get_all_data(self):
        dataset = self.col.find({})
        if dataset:
            return dataset
        else:
            return None