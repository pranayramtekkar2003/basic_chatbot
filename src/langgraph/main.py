import streamlit as st
from src.langgraph.LLM.groq_llm import GroqLLM
from src.langgraph.ui.streamlit.loadui import LoadStreamlitUI
from src.langgraph.ui.streamlit.resultDisplay import DisplayResultStreamlit
from src.langgraph.graph.graph_builder import GraphBuilder

def load_app():

    ui = LoadStreamlitUI()
    user_input = ui.load_ui()

    if not user_input:
        st.error("Error: Failed to load user input from the UI.")
        return
    
    user_message = st.chat_input("Enter your message:")

    if user_message:
        try:
            obj_llm = GroqLLM(user_control_input=user_input)
            model = obj_llm.get_llm_model()

            if not model:
                st.error("Error: LLM could not be initalized.")
                return
            
            usecase = user_input.get("selected_usecase")
            if not usecase:
                st.error("Error: No usecase selected")
                return
            

            builder = GraphBuilder(model)
            try:
                graph = builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase,graph,user_message).display_result()
            except Exception as e:
                st.error(f"Graph setup Failed: {e}")
                return

        except Exception as e:
            st.error(f"Setup Failed: {e}")
            return