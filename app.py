import streamlit as st
import requests
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np


from format import *

from scrape import return_approved
from scrape import name_drug
from scrape import generate_dan
from scrape import return_img_url

pd.set_option('display.max_colwidth', -1)



configure_page()
tab = toggle_sidebar()


if tab == "Home":
    #st.header("Drug Repurposing Navigator")
    display_logo()
    display_header(tab)
    
    cancers_list = [part + " Cancer" for part in ["Breast", "Ovarian", "Pancreatic", "Prostate"]]
    
                    
    cancer_type = st.selectbox("Select Cancer Type", cancers_list, key="sourceKey")
    
    option = cancer_type.split()[0].lower()
    
    url = "https://www.cancer.gov/about-cancer/treatment/drugs/" + option
    
    
    approved_drugs_list = return_approved(url)

    drug = st.selectbox(
        "Select a drug:", approved_drugs_list
    )
    
    if "mab" in drug.lower():
        st.markdown("""### Non-Chemical Drug""")
        st.write("This is an Antibody")
        
    else:
        
        text_contents = '''
                        Foo, Bar
                        123, 456
                        789, 000
                        '''
        st.write("\n\n\n")   
        
        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        
        with col4:
            st.download_button('Download CSV', text_contents, 'text/csv')
        
        st.markdown("### Generic Name")
        st.write(name_drug(drug))
    
        dan = generate_dan(drug)
        
        img_url = return_img_url(drug)
        
        st.markdown("### Chemical Structure")
        st.markdown(f"""![Alt Text]({img_url})""", unsafe_allow_html=True)
        
        st.markdown("### Research Status")
        st.write(state_drug_status(drug))
        
        st.markdown("### Chemical Formula")
        st.write(return_formula(drug))
        
        st.markdown("### Monoisotopic Weight")
        st.write(f"""{return_weight(drug)}""")
        
        st.markdown("### Targets")
        for target in return_targets(drug):
            st.write(target)
            
            
        st.markdown("### Enzymes")
        for enzyme in return_enzymes(drug):
            st.write(enzyme)
            
            
        st.markdown("### Transporters")
        for transporters in return_transporters(drug):
            st.write(transporters)
            
        st.markdown("### Similiar Structures")
        st.table(return_similar(drug))
        
        
        
        
        