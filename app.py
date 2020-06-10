import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open('model_gbc.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    gender=request.form['gender']
    age=request.form['age']
    height=request.form['height']
    weight=request.form['weight']
    ap_hi=request.form['ap_hi']
    ap_lo=request.form['ap_lo']
    cholesterol=request.form['cholesterol']
    gluc=request.form['gluc']
    smoke=request.form['smoke']
    alco=request.form['alco']
    active=request.form['active']

    final_values=[gender, age,height, weight, ap_hi, ap_lo,
                  cholesterol, gluc, smoke, alco, active]

    int_features = [int(x) for x in final_values]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output=''
    if prediction==0:
        output='Great! You are Healthy.'
    if prediction==1:
        output='Oops! You are suffering from Cardio Vascular Problems.'

    return render_template('index.html', prediction_text='{}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)