# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 06:14:48 2023

@author: Abdullah Syafiq
"""

import pandas as pd
import plotly.express as px
import streamlit as st


#%%

st.set_page_config(layout="wide")


# Functions for each of the pages
def home(uploaded_file):
    if uploaded_file:
        st.header('Begin exploring the data using the menu on the left')
    else:
        st.header('To begin please upload a file')
def amp_df():
    st.write('Amplification data')
    st.dataframe(amp)

def melt_df():
    st.write('Melting temperature data')
    st.dataframe(melt)
        
def melt_plot():
    col1, col2 = st.columns(2)
    
    target_filter = col1.selectbox('Select target', options=amp['target'].unique())
    dilution_filter = col2.selectbox('Select dilution', options=amp['dilution'].unique())

    filtered_df = melt[(melt['dilution'] == dilution_filter) & (melt['target'] == target_filter)]

    plot = px.line(filtered_df, x='temp', y='first_derivative',
                  color='id_combined',
                  line_group ='target',
                  line_dash  = 'group',
                 # line_dash  = 'target',
                 #symbol='dilution',
                 #title="Melting graph of C vs S (OXTR and GAPDH)",
                  )
    st.plotly_chart(plot, use_container_width=True)

def amp_plot():
    col1, col2 = st.columns(2)
    
    target_filter = col1.selectbox('Select target', options=amp['target'].unique())
    dilution_filter = col2.selectbox('Select dilution', options=amp['dilution'].unique())

    filtered_df = amp[(amp['dilution'] == dilution_filter) & (amp['target'] == target_filter)]

    plot = px.line(filtered_df, x='cycle', y='amplification',
                   color='group',
                   line_group ='id_combined',
                  # color='id_combined',
                  # line_group ='target',
                  # line_dash  = 'group',
                 # symbol='dilution',
                  title="Amplification graph of C vs S (OXTR and GAPDH)",
                  )
    st.plotly_chart(plot, use_container_width=True)
    

#%%
# Add a title and intro text
st.title("qPCR result explorer")
st.text("Welcome to Abdullah's qPCR result explorer webApp")

# Sidebar setup
st.sidebar.title('Sidebar')
upload_file_amp = st.sidebar.file_uploader('Upload a file containing qPCR amplification data')
upload_file_melt = st.sidebar.file_uploader('Upload a file containing qPCR melting data')

#Sidebar navigation
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select what you want to display:', 
                           ['Home','Melting curve', 'Amplification curve',
                            'Melting data','Amplification data'])
#%%

# Check if file has been uploaded
if ((upload_file_amp is not None) & (upload_file_melt is not None)):
    amp = pd.read_csv(upload_file_amp)
    melt = pd.read_csv(upload_file_melt)
    
# Navigation options
if options == 'Home':
    home(upload_file_amp)
elif options == 'Melting curve':
    melt_plot()
elif options == 'Amplification curve':
    amp_plot()
elif options == 'Melting data':
    melt_df()
elif options == 'Amplification data':
    amp_df()
