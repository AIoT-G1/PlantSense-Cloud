from joblib import dump, load

class rain_predictor:
     
    def predict(self, temperature, humidity):
        
        try:
            
            # predict new temperature and humidity observation
            clf = load('rain-classifier.joblib')
            print("to predict --> temp: " + str(temperature) + " ; humidity: " + str(humidity))
            # temperature, humidity
            newX = [[temperature, humidity]]
            result = clf.predict(newX)
            print('Predict Rain: temp={}; humidity={}; rain={}'.format(temperature, humidity, result[0]))

            return str(result[0])
            
        except Exception as error:

            return 'Unknown'