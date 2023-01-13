import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="house"
)

with open("style.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

st.title("WJP GPP Interactive Data Map")
st.markdown(
    """
    <p class='jtext'>
    This is an interactive app designed to display the most important information related to the questions/variables
    that you can find in the different waves of the General Population Polls between 2018 and 2022. This app is designed 
    to help you find a variable in the dataset along with its most important details such as available years, encoding,
    available countries, among other information. 
    </p>
    
    <p class='jtext'>
    In order to find a variable, you can either search it using a <strong style="color:#003249">keyword</strong> or, if
    you don't have a keyword, you could also <strong style="color:#003249">explore</strong> the GPP catalog in order to 
    filter variables by topic and availability. You will find both methods in the left side panel of this website.
    </p>

    <p class='jtext'>
    If you have questions, suggestions or you want to report a bug, make sure of checking the 
    <strong style="color:#003249">Info Tab</strong> in the left side bar panel.
    </p>

    <p class='jtext'>
    Galingan!
    </p>
    """,
    unsafe_allow_html = True
)
