import streamlit as st

# Page config
st.set_page_config(
    page_title="info",
    page_icon="house"
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
    <p class='jtext'>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore 
    magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo 
    consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
    Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </p>
    """,
    unsafe_allow_html = True
)