# WJP GPP Interactive Data Map

Python repository containing the source code for the an interactive tool that allows the user to quickly locate and get information on questions from the General Population Polls gathered by the World Justice Project. The app was programmed entirely in Python using the [Streamlit](https://streamlit.io/) web framework. 

* Last available version: May 8th, 2023

![]("Media/home.png")

## Filing system
The tool is designed to be a multipage app. As such, in the root directory you will find the `1_Home.py` script containing the code for the home page of the app, while in the `/pages/` sub-directory you can find the cod for the remaining pages of the app. In the `/Data/` sub-directory you can find the data that serves as baase for the app as CSV files. A `styles.css` file is added for aesthetic purposes.

## Deployment
The app has been deployed online using the [Streaamlit Community Cloud](https://streamlit.io/cloud) services and can be found in [this link](https://gpp-datamap.streamlit.app/).


