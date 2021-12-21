import streamlit as st
from scrape import *
from PIL import Image


image = Image.open("logo.png")
pd.set_option('display.max_colwidth', -1)



def clear_page():
    hide_st_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                 """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    
def configure_page():
    st.set_page_config(page_title="Drug Repurposing", layout="wide", page_icon=image, initial_sidebar_state="collapsed")
    
    clear_page()

def center_align(item):
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col3.image(item, width=300)
    

def display_logo():
    center_align(image)
    
    
def toggle_sidebar():
    menu = ["Home", "Download"]
    tab = st.sidebar.selectbox("Drug Repurposing", menu)
    
    return tab

def display_header(tab):
    st.subheader(tab.upper())
    
