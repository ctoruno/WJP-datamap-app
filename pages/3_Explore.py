import pandas as pd
import numpy as np
import re
import streamlit as st
import streamlit.components.v1 as stc

# Page config
st.set_page_config(
    page_title = "Explorer",
    page_icon  = "🧭"
)

# CSS Style
with open("style.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Cache of data
@st.cache_data
def load_data():
    # Loading data
    data = pd.read_csv("Data/datamap.csv")
    return data 

# Loading data frame
datamap = load_data()

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Explorer Tool</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Welcome to the <strong style="color:#003249">explorer tool</strong>. In this page you can search questions
    in the data map based on thematic groups and availability. It is not necessary to fill the country-year
    filters in order to get results. However, they will narrow your search.
    </p>
    """,
    unsafe_allow_html = True
)

# Listing filters
module_list = sorted(datamap.module.unique())

availability_list = (datamap
                     .loc[datamap["name"] == "gend", "availability"]
                     .values.item()
                     .split(", "))
all_countries = (np
                 .unique([re.sub("(?<=-).*|-", "", string) for string in availability_list])
                 .tolist())
all_years = (np
             .unique([re.sub(".*(?=[0-9]{4})|[a-zA-Z\s]", "", string) for string in availability_list])
             .tolist())
all_years = list(filter(None, all_years))

# Search Box Inputs
with st.form(key = "searchform"):
    st.markdown("<h4>Step 1: Choose a thematic module</h4>",
                unsafe_allow_html = True)
    modules = st.multiselect("Select a thematic module from the following list:",
                             module_list,
                             default = None,
                             help    = "HOLA")
    st.markdown("<h5>Step 2 (Optional): Further filter your results</h5>",
                unsafe_allow_html = True)
    countries = st.multiselect("Available for the following countries:",
                               all_countries,
                               default = None)
    years = st.multiselect("Available for the following years:",
                           all_years,
                           default = None)
    submit_button = st.form_submit_button(label = "Search!")

# Server
if submit_button:

    # Filtering results by selected modules
    results = datamap[datamap.module.isin(modules)]

    # Further filtering results if they filled the country-year filters
    if countries != []:
        country_keys = "|".join(countries)
        results = results[results.availability.str.contains(country_keys, case = False)]
    
    if years != []:
        year_keys = "|".join(years)
        results = results[results.availability.str.contains(year_keys, case = False)]

    # Success Box
    nresults = len(results.index)
    st.success(f"Your search returned {nresults} results.")

    for index, row in results.iterrows():

        with st.container():
            vname = row["merge"]
            vyears = row["available_years"]
            vanswers = row["values"]
            vcountries = row["available_countries"]
            description = row["description"]

            variable_html_layout = f"""
                                    <div>
                                    <h4>{vname}</h4>
                                    <p class='jtext'><strong>Description:</strong></p>
                                    <p class='vdesc'>{description}</h4>
                                    </div>
                                    """
            
            st.markdown(variable_html_layout,
                        unsafe_allow_html=True)
            
            with st.expander("Coded Answers"):
                stc.html(vanswers, 
                         scrolling=True)
            with st.expander("Available Countries"):
                stc.html(vcountries, scrolling=True)
            with st.expander("Available Years"):
                stc.html(vyears, scrolling=True)
        
        st.markdown("---")