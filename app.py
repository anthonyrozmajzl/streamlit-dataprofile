import numpy as np
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os

print(type(sys))

st.set_page_config(page_title = 'Data Profile', layout='wide')


def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_MB = size_bytes / (1024**2)
    return size_MB


def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        False

# sidebar

with st.sidebar:
    uploaded_file = st.file_uploader("Upload .csv or .xlsx files not exceeding 10MB")
    if uploaded_file is not None:
        st.write('Modes of Operation')
        minimal = st.checkbox("Minimal Report?")
        display_mode = st.radio('Display Mode',('Primary','Dark','Orange'))

        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode = True
        else:
            dark_mode = False
            orange_mode = False
    

if uploaded_file is not None:
    ext = validate_file(uploaded_file)
    if ext:
        filesize = get_filesize(uploaded_file)
        if filesize <= 10:

            if ext =='.csv':
        # load csv
                df = pd.read_csv(uploaded_file)
            else:
                xl_file = pd.ExcelFile(uploaded_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet', sheet_tuple)
                df = xl_file.parse(sheet_name)
        # generate report
            with st.spinner("Generating report"):
                pr = ProfileReport(df,
                            minimal=minimal, 
                            dark_mode=dark_mode,
                            orange_mode=orange_mode
                            )
        
            st_profile_report(pr)
            st.success("Report has been generated")
        else:
            st.error(f'Maximum file size cannot exceed 10MB. Current file size: {int(filesize)} MB')
    else:
        st.error('Must upload a .csv or .xlsx file')
else:
    st.title('Data Profiler')
    st.info('Upload your data in the left sidebar to generate a profile report')