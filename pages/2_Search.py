import pandas as pd
import numpy as np
import re
from PIL import Image
import streamlit as st
import streamlit.components.v1 as stc

# Page config
st.set_page_config(
    page_title = "Search Tool",
    page_icon  = "🔍"
)

# CSS Style
with open("style.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Loading examples
example1 = Image.open("Media/example1.png")
example2 = Image.open("Media/example2.png")

# Cache of data
@st.cache_data
def load_data():
    # Loading data
    data = pd.read_csv("Data/datamap.csv")
    return data 

# Loading data frame
datamap = load_data()

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Search Assistant</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <h5>Read me first...</h5>

    <p class='jtext'>
    Welcome to the <strong style="color:#003249">search assistant</strong>. In this page you can search for a question
    in the data map based on keywords and availability. It is not necessary to fill the filters in order to get results.
    However, they will narrow your search.
    </p>

    <p class='jtext'>
    There are <strong style="color:#003249">two ways</strong> of finding that specific question you don't remember:
    </p>
    <ol>
        <li>... by its name in the data set, or</li>
        <li>... by their description.</li>
    </ol>

    <p class='jtext'>
    If this is your first time using this app, please check the following examples:
    </p>
    """,
    unsafe_allow_html = True
)

examples = st.expander("Click here to see the search examples:")
with examples:

    ex1, ex2 = st.tabs(["Example 1", "Example 2"])

    with ex1:
        st.markdown(
        """
        <p class='jtext-ex'>
        <b>Search by variable name:</b>
        </p>

        <p class='jtext-ex'>
        If you know the name of a variable such as "CAR_q43" and you want to read its description, 
        the value encoding and its availability, then you can directly type it in the keywords text box and click 
        <strong style="color:#003249">Search!</strong>. Note that the name of the variable is the name that the question 
        has in the data set (<i>merged.dta</i>), not in the paper questionnaire.
        </p>
        """,
        unsafe_allow_html = True
        )

        st.image(example1)

    with ex2:
        st.markdown(
        """
        <p class='jtext-ex'>
        <b>Search by variable description:</b>
        </p>

        <p class='jtext-ex'>
        On the other hand, if you would like to see which questions are related to -for example- trust in the police and 
        public defense attorneys, then you need to tick the <strong style="color:#003249">"Search variables by 
        description"</strong> checkbox, write "trust police OR attorney" in the keywords text box and then click on
        the <strong style="color:#003249">Search!</strong> button. Note that if you don't use the OR (upper caps)
        logical operand, it will search for questions that has the words "police" AND "attorney" in their
        description, while what we want is to search questions that has both "police" OR "attorney"
        in their description.
        </p>
        """,
        unsafe_allow_html = True
        )
        st.image(example2)

st.markdown("------")

# Listing all posible availabilities: countries and years
# I choose "gend" as a reference becaause this variable is available across all the dataset
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

# Writing helpers
keywords_hlp = """
The app will search questions (either by their name or their description) based in the keywords defined in this 
text box.
"""

chkbox_hlp = """
By default, the app will search for questions whose name match the provided keywords. However, if you would like
your search to be based on variable descriptions instead of variable names, then make sure to tick this box.
"""

# Search Box Inputs
with st.form(key = "searchform"):
    st.markdown("<h4>Step 1: Search questions based on:</h4>",
                unsafe_allow_html = True)
    keywords = st.text_input("The following keywords:",
                             help = keywords_hlp)
    target = st.checkbox(label = "Search variables by description",
                         help = chkbox_hlp)
    
    st.markdown("<h5>Step 2: Further filter your results by showing questions that are...</h4>",
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

    # Transforming keywords
    keys = []
    keywords = re.sub(" OR ", "|", keywords)
    for key in keywords.split():
        regexkey = f"(?=.*{key})"
        keys.append(regexkey)
    keys = "^" + "".join(keys)

    # Filtering data frame
    if target == False:
        targetCol = "merge"
    else: 
        targetCol = "description"

    results = datamap[datamap[targetCol].str.contains(keys, case = False)]

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
        


