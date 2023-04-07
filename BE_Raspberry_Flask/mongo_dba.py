from pymongo import MongoClient, DESCENDING

class mongo_dba:
    def __init__(self, collection):

        self.host = 'localhost'
        self.port = 27017
        self.con = MongoClient(self.host, self.port)
        self.db = self.con.plantsense
        
        if collection == "plant_sensor_data":
            self.col = self.db.plant_sensor_data
        if collection == "plant_info":
            self.col = self.db.plant_info
        if collection == "system_sensor_data":
            self.col = self.db.system_sensor_data
        if collection == "last_watered":
            self.col = self.db.last_watered

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
    
    def update_last_watered(self, data):
        print(data)
        
        find = self.col.find_one({'plant_node_id': data['plant_node_id']})
        
        if find == None:
            output = self.col.insert_one({'plant_node_id': data['plant_node_id'],
                                          'watering_history': [data['timestamp']]})
        else:
            output = self.col.update_one(
                {'plant_node_id': data['plant_node_id']},
                {'$push': {'watering_history': data['timestamp']}}
            )
        
        print(str(output))
        
    def update_plant_info(self, data):
        print(data)
        find = self.col.find_one({'plant_node_id': data['plant_node_id']})

        if find == None:
            output = self.col.insert_one(data)
        else:
            output = self.col.update_one(
                {'plant_node_id': data['plant_node_id']},
                {'$set': data}, upsert=True
            )

        print(str(output))
        
    def update_system_data(self, data):
        print(data)
        output = self.col.insert_one(data)

        print(str(output))
        
        
        
    