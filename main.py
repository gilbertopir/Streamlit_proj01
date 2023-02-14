import streamlit as st
import sopscalc as sp
import csv2dxf

import pandas as pd
#import numpy as np



with st.container():
#st.set_page_config(layout="wide")
  st.image("https://www.tonygee.com/wp-content/uploads/2021/06/SocialImg.jpg",width=250)
  st.title("TonyGee Automation Services")
  st.write("---")
  st.header("TRU Lineside Civils")
  st.subheader("Advanced Setting Out Generator and CAD QA")
  st.write("---")
  st.subheader("Asset: Trough Foundation")


with st.container():
  form = st.form(key='my_form')
  sops = form.text_area('Please paste output report from Microstation BIM model','''Level,Top
  CV-CV-Foundation-G-P (Proposed Foundations),247334.1921m, 435864.1390m, 76.8240m
  CV-CV-Foundation-G-P (Proposed Foundations),247329.9031m, 435860.3310m, 76.8241m
  CV-CV-Foundation-G-P (Proposed Foundations),247338.6784m, 435868.1231m, 76.8239m
  CV-CV-Foundation-G-P (Proposed Foundations),247343.1647m, 435872.1072m, 76.8240m
  CV-CV-Foundation-G-P (Proposed Foundations),247346.2363m, 435875.0225m, 76.8239m
  CV-CV-Foundation-G-P (Proposed Foundations),247349.6008m, 435878.0103m, 76.8239m
  CV-CV-Foundation-G-P (Proposed Foundations),247352.1374m, 435880.0754m, 76.8240m
  CV-CV-Foundation-G-P (Proposed Foundations),247356.5372m, 435884.1552m, 76.7926m
  ''',height=250)
  submit = form.form_submit_button(label='Submit')
  if submit:
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    
    st.write('Session status: Data received')
    with open('List.csv', 'w') as f:
      f.write(sops)    
    st.write('Session status: Data file recorded')
    my_bar.progress(10, text=progress_text)
    
    sp.sortListFile()
    st.write('Session status: Data sorted')
    my_bar.progress(20, text=progress_text)
    
    sp.run()
    st.write('Session status: Data computed')
    my_bar.progress(80, text=progress_text)
    
    sp.sortEndFile()
    st.write('Session status: Data re-sorted')
    my_bar.progress(90, text=progress_text)
    
    csv2dxf.csvtodxf()
    st.write('Session status: CAD QA file created')
    my_bar.progress(100, text=progress_text)

    df = pd.read_csv("_SOP_report_.csv")
    st.dataframe(df)  # Same as st.write(df)

    #with open('_SOP_report_.csv', 'rb') as f:
    #  st.download_button('Download CSV', f, file_name='_SOP_report_.csv')
    with open('Report_QA.dxf', 'rb') as f:
      st.download_button('Download DXF QA', f, file_name='Report_QA.dxf')
    
  else:
      st.write('Session status: No new data received')

