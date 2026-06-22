import streamlit as st

from src.langgraph.ui.streamlit.loadui import LoadStreamlitUI

def load_app():

    ui = LoadStreamlitUI()
    user_input = ui.load_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        pass