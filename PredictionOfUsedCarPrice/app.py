from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask("car_model")
model = pickle.load(open("randomforest.pickle", 'rb'))

@app.route('/',methods=['GET'])

def Home():
    return render_template('index.html')

standard_to = StandardScaler()

@app.route("/predict", methods=['POST'])

def predict():

    if request.method == 'POST':

        Year = int(request.form['Year'])
        Year = 2020 - Year

        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)

        Owner = int(request.form['Owner'])
        Seats = int(request.form['Seats'])
        Mileage = int(request.form['Mileage'])
        ECC = int(request.form['ECC'])
        BHP = int(request.form['BHP'])

        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']

        if (Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
            Fuel_Type_Lpg = 0
        elif (Fuel_Type_Petrol == 'Diesel'):
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
            Fuel_Type_Lpg = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0
            Fuel_Type_Lpg = 1

        Transmission_Manual = request.form['Transmission_Manual']
        if (Transmission_Manual == 'Mannual'):
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        prediction=model.predict([[Year,Kms_Driven2,Owner,Seats,Mileage,ECC,BHP,Fuel_Type_Diesel,Fuel_Type_Lpg,Fuel_Type_Petrol,Transmission_Manual]])
        output=round(prediction[0],2)

        if output<0:
            return render_template('index.html',prediction_text="❌ Sorry you cannot sell this car. 🙁")
        else:
            return render_template('index.html',prediction_text="✅ Predicted Car Price {} lakhs 🤑👍".format(output))

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
