import streamlit as st

# Page config
st.set_page_config(
    page_title = "Info",
    page_icon  = "⛩️"
)

# CSS Style
with open("style.css") as stl:
    st.markdown(f"<style>{stl.read()}</style>", 
                unsafe_allow_html=True)

# Header and explanation
st.markdown("<h1 style='text-align: center;'>Information</h1>", 
            unsafe_allow_html=True)
st.markdown(
    """
    <b>Author(s):</b> 
    <ul>
        <li>Carlos Alberto Toruño Paniagua</li>
    </ul>

    <h4>Source Code:</h4>
    <p class='jtext'>
    The GPP Data Map Tool was programmed entirely in Python using the <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    web framework. The code is publicly available in this 
    <a href="https://github.com/ctoruno/WJP-datamap-app" target="_blank">GitHub Repository</a>.
    </p>

    <h4>Data:</h4>
    <p class='jtext'>
    The data and information contained in this app is partly based on the publicly available questionnaires published 
    by the <strong style="color:#003249">World Justice Project</strong>. You can check these questionnaires on 
    <a href="https://worldjusticeproject.org/rule-of-law-index/downloads/Questionnaires_2022.zip" target="_blank">
    here
    </a>,
    <a href="https://worldjusticeproject.org/sites/default/files/documents/Caribbean_GPP_Questionnaire_2022_English.pdf" 
    target="_blank">
    here
    </a> and 
    <a href="https://worldjusticeproject.org/sites/default/files/documents/Central%20America%20GPP%20Questionnaire%202022_English.pdf"
    target="_blank">
    here
    </a>.
    </p>

    <h4>Disclaimer:</h4>

    <p class='jtext'>
    The information provided in this online tool is for general informational purposes only. While the previously
    stated author(s) strive to provide accurate and up-to-date information, we make no representations or 
    warranties of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or 
    availability with respect to the information, products, services, or related data contained in this app 
    for any purpose. Any reliance you place on such information is therefore strictly at your own risk.
    </p>

    <p class='jtext'>
    Please note that the data presented in this online tool <b>SHOULD NOT</B> be taken as 
    official information from the <strong style="color:#003249">World Justice Project</strong>, 
    and any errors or omissions are solely the responsibility of the previously stated author(s).
    For the latest official information available you should visit the 
    <a href="https://worldjusticeproject.org/" target="_blank">
    official website of the World Justice Project
    </a>.
    </p>

    <p class='jtext'>
    This online tool is a personal project of the  previously stated author(s). Every effort is made to keep 
    the tool up and running smoothly. The <strong style="color:#003249">World Justice Project</strong> takes no 
    responsibility for, nor will be liable for any information displayed in this app or by the unavailability or
    interruption in its service.
    </p>

    <p class='jtext'>
    The inclusion of any links in this online tool does not necessarily imply a recommendation or endorse 
    the views expressed within them.
    </p>

    <h4>License:</h4>
    The GPP Data Map Tool is an open-source application that is licensed under the Creative Commons 
    Attribution-NonCommercial 4.0 International license. This means that anyone is free to use, modify, and 
    distribute the software, subject to the terms and conditions of the previously stated license.
    By using this online tool, you acknowledge and agree to be bound by the terms and conditions of the 
    Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.

    """,
    unsafe_allow_html = True
)