from joblib import dump, load


class rain_predictor:

    def predict(self, temperature, humidity):

        try:

            temperature = float(temperature)
            humidity = float(humidity)
            print("1")
            # predict new temperature and humidity observation
            clf = load('rain-classifier.joblib')
            print("2")
            print("to predict --> temp: " +
                  str(temperature) + " ; humidity: " + str(humidity))
            # temperature, humidity
            newX = [[temperature, humidity]]
            result = clf.predict(newX)
            print("3")
            print('Predict Rain: temp={}; humidity={}; rain={}'.format(
                temperature, humidity, result[0]))
            
            return str(result[0])

        except Exception as error:

            return 'Unknown'
