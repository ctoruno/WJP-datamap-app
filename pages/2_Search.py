import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
import re

# Page config
st.set_page_config(
    page_title="Home",
    page_icon="house"
)

# CSS Style
with open("style.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Loading data frame
datamap = pd.read_csv("Data/datamap.csv")

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Search Assistant</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <p class='jtext'>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore 
    magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
    consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>
    """,
    unsafe_allow_html = True
)

all_countries = datamap.loc[datamap["name"] == "gend", "available_countries"]
all_countries = all_countries.values.item()
all_countries = all_countries.split("; ")

# Search Box Inputs
with st.form(key = "searchform"):
    st.markdown("<h4>Search questions based on:</h4>",
                unsafe_allow_html = True)
    keywords = st.text_input("The following keywords:")
    countries = st.multiselect("Available for the following countries:",
                               all_countries,
                               default = None)
    years = st.multiselect("Available for the following years:",
                           ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"],
                           default = None)
    submit_button = st.form_submit_button(label = "Search!")


# Server
if submit_button:

    # Transforming keywords
    keys = []
    for key in keywords.split():
        regexkey = f"(?=.*{key})"
        keys.append(regexkey)
    keys = "^" + "".join(keys) + ".*$"

    # Filtering data frame
    results = datamap[datamap.text.str.contains(keys, case = False)]

    if countries != []:
        country_keys = "|".join(countries)
        results = results[results.available_countries.str.contains(country_keys, case = False)]
    
    if years != []:
        year_keys = "|".join(years)
        results = results[results.available_years.str.contains(year_keys, case = False)]

    # Success Box
    nresults = len(results.index)
    st.success(f"Your search returned {nresults} results.")

    for index, row in results.iterrows():

        with st.container():
            vname = row["name"]
            vyears = row["available_years"]
            vanswers = row["answers"]
            vcountries = row["available_countries"]
            description = row["text"]

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
                stc.html(vanswers, scrolling=True)
            with st.expander("Available Countries"):
                stc.html(vcountries, scrolling=True)
            with st.expander("Available Years"):
                stc.html(vyears, scrolling=True)
            with st.expander("Questionnaire labels"):
                st.write(results.loc[results["name"] == row["name"], "label_2018":"label_EXP22"])
        
        st.markdown("---")
        

