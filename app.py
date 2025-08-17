
from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            Year = int(request.form['Year'])
            Present_Price = float(request.form['Present_Price'])
            Kms_Driven = int(request.form['Kms_Driven'])
            Kms_Driven2 = np.log(Kms_Driven)
            Owner = int(request.form['Owner'])

            Fuel_Type = request.form['Fuel_Type_Petrol']
            if Fuel_Type == 'Petrol':
                Fuel_Type_Petrol = 1
                Fuel_Type_Diesel = 0
            elif Fuel_Type == 'Diesel':
                Fuel_Type_Petrol = 0
                Fuel_Type_Diesel = 1
            else:
                Fuel_Type_Petrol = 0
                Fuel_Type_Diesel = 0

            Year = 2020 - Year

            Seller_Type = request.form['Seller_Type_Individual']
            if Seller_Type == 'Individual':
                Seller_Type_Individual = 1
            else:
                Seller_Type_Individual = 0

            Transmission = request.form['Transmission_Mannual']
            if Transmission == 'Mannual':
                Transmission_Mannual = 1
            else:
                Transmission_Mannual = 0

            prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
            output = round(prediction[0], 2)
            if output < 0:
                return render_template('index.html', prediction_text="Sorry you cannot sell this car")
            else:
                return render_template('index.html', prediction_text="You Can Sell The Car at {} lakhs".format(output))
        except Exception as e:
            return render_template('index.html', prediction_text="Error: {}".format(str(e)))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

import os
port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=port)

