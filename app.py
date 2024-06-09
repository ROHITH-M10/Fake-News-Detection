import streamlit as st
import pandas as pd
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from statistics import mode



ps = PorterStemmer()

def stemming(text):
    stemming_text = re.sub('[^a-zA-Z]', ' ', text)
    stemming_text = stemming_text.lower()
    stemming_text = stemming_text.split()
    temp_stemming_text_list = []
    for word in stemming_text:
        if word not in stopwords.words('english'):
            temp_stemming_text_list.append(ps.stem(word))
    stemming_text = ' '.join(temp_stemming_text_list)
    return stemming_text



model_lr = joblib.load('model_lr.pkl')
model_dt = joblib.load('model_dt.pkl')
model_rf = joblib.load('model_rf.pkl')
vector = joblib.load('vectorizer.pkl')

print(model_dt)


st.title(':blue[Real or Fake News Prediction]')
st.divider()

st.header('Enter the news to check if it is Real or Fake')
user_input = st.text_area("")

if st.button('Predict'):
    if user_input == "":
        st.subheader(':large_yellow_square: Please enter the news')
    else:
        user_input = stemming(user_input)
        user_input = [user_input]
        user_input = vector.transform(user_input)

        user_input_pred_lr = model_lr.predict(user_input)
        user_input_pred_dt = model_dt.predict(user_input)
        user_input_pred_rf = model_rf.predict(user_input)

        


        user_input_pred = mode([user_input_pred_lr[0], user_input_pred_dt[0], user_input_pred_rf[0]])

        if user_input_pred == 0:
            st.subheader(':large_red_square: This is a Fake News')
        else:
            st.subheader(':large_green_square: This is a Real News')

        
        pred_df = pd.DataFrame({
                'Model': ['Logistic Regression', 'Decision Tree', 'Random Forest'],
                'Prediction': [user_input_pred_lr[0], user_input_pred_dt[0], user_input_pred_rf[0]]
                })

        st.dataframe(pred_df)





# CSS
st.markdown(
    """
    <style>
    h1{
        color: cyan;
    }
    textarea {
        font-size: 1.2rem !important;
    }
    hr{
        border-color: grey;
    }
    </style>
    """,
    unsafe_allow_html=True,
)