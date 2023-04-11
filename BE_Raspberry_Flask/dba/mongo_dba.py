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
        if collection == "weather":
            self.col = self.db.weather
        if collection == "water_tank":
            self.col = self.db.water_tank

# Collection Fx --> Plant sensor data
    def get_last_sensor_values(self):
        dataset = self.col.find({}, {'_id':0, 'action': 0})
        if dataset:
            return list(dataset)
        else:
            return None

    def add_plant_sensor_data(self, data):
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


# Collection Fx --> Plant information
    def get_all_plant_info(self):
        dataset = self.col.find({}, {'_id':0, 'action': 0})
        if dataset:
            return list(dataset)
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
        
    def update_last_image(self, data):
        print(data)
        find = self.col.find_one({'plant_node_id': data['plant_node_id']})

        if find == None:
            output = self.col.insert_one(data)
        else:
            output = self.col.update_one(
                {'plant_node_id': data['plant_node_id']},
                {'$set': data}
            )

        print(str(output))
            

# Collection Fx --> Weather 
    def add_weather_data(self, data):
        print(data)
        self.col.insert_one(data)
        
    def get_last_weather_data(self):
        output = self.col.find_one(sort=[( '_id', DESCENDING )], projection ={'_id': 0, 'action': 0})
        if output:
            return output
        else:
            return None


# Collection Fx --> Water tank    
    def update_water_tank(self, data):
        print(data)
        find = self.col.find_one({})

        if find == None:
            output = self.col.insert_one(data)
        else:
            output = self.col.update_one(
            {},{'$set': data}, upsert=True
            )

        print(str(output))
        
    def get_water_tank_level(self):
        output = self.col.find_one({}, {'_id': 0, 'action': 0})
        if output:
            return output
        else:
            return None
        
# UTILS ->  Response formatter
    def format_response(self, data):
        for value in data:
            if(isinstance(data[value], str)==False):
                data[value]=str(data[value])
        return data
        
        
        
    