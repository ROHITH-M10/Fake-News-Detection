from flask import Flask, request, jsonify
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask_cors import CORS
from statistics import mode


app = Flask(__name__)
CORS(app)
ps = PorterStemmer()


model_lr = joblib.load('model_lr.pkl')
model_dt = joblib.load('model_dt.pkl')
model_rf = joblib.load('model_rf.pkl')
vector = joblib.load('vectorizer.pkl')

@app.route('/', methods=['GET'])
def get_home():
    data = {
        "message" : "API is running"
    }
    return jsonify(data)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        data = str(request.get_json())
        
        stemming_text = re.sub('[^a-zA-Z]', ' ', data)
        stemming_text = stemming_text.lower() 
        stemming_text = stemming_text.split(' ')
        
        temp_stemming_text_list = []
        for word in stemming_text:
            if word not in stopwords.words('english') and word != '':
                temp_stemming_text_list.append(ps.stem(word))
        # stemming_text = ' '.join(temp_stemming_text_list)
        
        processed_text = ' '.join(temp_stemming_text_list)
        transformed_text = vector.transform([processed_text])

        

        pred_lr = model_lr.predict(transformed_text)[0]
        pred_dt = model_dt.predict(transformed_text)[0]
        pred_rf = model_rf.predict(transformed_text)[0]

        pred_lr = int(pred_lr)
        pred_dt = int(pred_dt)
        pred_rf = int(pred_rf)


        pred_sum = pred_lr + pred_dt + pred_rf
        """
        if atleast 2 models predict the news as fake then the news is fake
        else the news is real
        real is 1 and fake is 0
        so if the sum is greater than 1 then the news is real
        """
        if pred_sum > 1:
            pred = 1
        else:
            pred = 0
    

        if pred == 1:
            prediction = "The news is Real"
        else:
            prediction = "The news is Fake"
        return jsonify({
            "prediction": prediction
        })
        
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
