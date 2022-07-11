from indeed import get_jobs as get_indeed_jobs
import pandas as pd
import streamlit as st

search_term = st.text_input("What kind of Jobs you are looking for?")
if st.button("Find"):   
    indeed_jobs = get_indeed_jobs(search_term)
    st.write(pd.DataFrame(indeed_jobs))