import pandas as pd
import streamlit as st
import os
from io import BytesIO

#app set up
st.set_page_config(page_title="Data sweeper", layout="wide")
st.title("Data sweeper")
st.write("Transform your files between CVS and Excel format with built in data cleaning and visualization!")
uploaded_files = st.file_uploader("upload your files (CVS or Excel):", type=["csv", "xlsx"],
accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
             df = pd.read_excel(file)
        else:
            st.error(f"Unssupported file type : {file_ext}")
            continue
        
        #display file info
        st.write(f"**File name** : {file.name}")
        st.write(f"**File size** : {file.size/1024}")
        
        #show 5 rows of df (data frame)
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())
        
        #Options for data cleaning 
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
                    
            with col2:
               if st.button(f" Fill Missing Values for {file.name}"):
                   numeric_cols = df.select_dtypes(include=['number']).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("missing Values have been filled!")
        
        # Specific coulums to keep and convert
        st.subheader("select specific coulumns to convert")
        columns= st.multiselect(f"Choose coulumns for {file.name}", df.columns,default = df.columns)
        df = df[columns]
        
        #Create some visualization 
        st.subheader(f"📂 File visualization for {file.name}")
        if st.checkbox (f"Show visualization for numeric data in {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
            
        # Convert the file logic
        
        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:" , ["CSV", "Excel"]  , key=file.name)
        if st.button (f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer , index=False)
                file_name = file.name.replace (file_ext, ".csv")
                mime_type = "text/csv"
                st.success("✨ files are processed")
             
            elif conversion_type == "Excel":
                df.to_excel(buffer , index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                st.success("✨ files are processed")
            buffer.seek(0)
            
            #Download button
            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name= file_name,
                mime = mime_type
            )

