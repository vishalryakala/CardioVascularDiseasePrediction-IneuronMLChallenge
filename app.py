import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import logging

logging.basicConfig(filename='appLogs.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)
try:
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    logging.error('.pkl not found')

@app.route('/')
def home():
    return render_template('index.html')
    logging.error('Index html rendered Successfully')

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
    logging.info('gender read as {}'.format(gender))
    logging.info('age read as {}'.format(age))
    logging.info('height read as {}'.format(height))
    logging.info('weight read as {}'.format(weight))
    logging.info('ap_hi read as {}'.format(ap_hi))
    logging.info('ap_lo read as {}'.format(ap_lo))
    logging.info('cholesterol read as {}'.format(cholesterol))
    logging.info('gluc read as {}'.format(gluc))
    logging.info('smoke read as {}'.format(smoke))
    logging.info('alco read as {}'.format(alco))
    logging.info('active read as {}'.format(active))


    final_values=[gender, age,height, weight, ap_hi, ap_lo,
                  cholesterol, gluc, smoke, alco, active]

    int_features = [int(x) for x in final_values]
    logging.info('converted all read values to int features')
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    logging.info('Model Predicted as {}'.format(prediction))

    output=''
    if prediction==0:
        output='You are Healthy'
    if prediction==1:
        output='You are suffering from Cardio Vascular Problems'

    return render_template('index.html', prediction_text='{}'.format(output))
    logging.info('Rendered result as {}'.format(output))



if __name__ == "__main__":
    app.run(debug=True)