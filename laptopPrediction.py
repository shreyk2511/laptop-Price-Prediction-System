import streamlit as st
import pickle
import numpy as np

# import the model
pipe = pickle.load(open('fpipe1.pkl','rb'))
df = pickle.load(open('fdf.pkl','rb'))

st.title("Laptop Predictor")

# brand
company = st.selectbox('Brand',df['Company'].unique())

# type of laptop
type = st.selectbox('Type',df['TypeName'].unique())

# Ram
ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight of the Laptop')



#cpu
cpu = st.selectbox('CPU',df['Cpu brand'].unique())

hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])


gpu = st.selectbox('GPU',df['Gpu brand'].unique())

os = st.selectbox('OS',df['os'].unique())

if st.button('Predict Price'):
    query = np.array([company,type,ram,weight,cpu,hdd,gpu,os])

    query = query.reshape(1,8)
    st.title("The predicted price of this configuration is " + str(int(np.exp(pipe.predict(query)[0]))))
