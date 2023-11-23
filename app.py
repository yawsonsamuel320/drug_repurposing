# Import necessary libraries
import streamlit as st
import requests
import subprocess
import sys

# Function to install BeautifulSoup if not already installed
def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])

# Try to import BeautifulSoup, install it if not successful
try:
    from bs4 import BeautifulSoup
except:
    install_bs4()
    from bs4 import BeautifulSoup

import pandas as pd
import numpy as np

# Import functions from custom modules
from format import *
from scrape import return_approved, name_drug, generate_dan, return_img_url

# Set Pandas display options
pd.set_option('display.max_colwidth', None)

# Configure Streamlit page settings
configure_page()

# Create a toggle sidebar and get the selected tab
tab = toggle_sidebar()

# Display content based on the selected tab
if tab == "Home":
    # Display logo and header
    display_logo()
    display_header(tab)
    
    # Create a list of cancer types
    cancers_list = [part + " Cancer" for part in ["Breast", "Ovarian", "Pancreatic", "Prostate"]]
                    
    # Create a dropdown to select cancer type
    cancer_type = st.selectbox("Select Cancer Type", cancers_list, key="sourceKey")
    
    # Extract the option from the selected cancer type
    option = cancer_type.split()[0].lower()
    
    # Construct the URL for the selected cancer type
    url = "https://www.cancer.gov/about-cancer/treatment/drugs/" + option
    
    # Get a list of approved drugs for the selected cancer type
    approved_drugs_list = return_approved(url)

    # Create a dropdown to select a drug from the approved list
    drug = st.selectbox("Select a drug:", approved_drugs_list)
    
    # Check if the selected drug is an antibody
    if "mab" in drug.lower():
        st.markdown("""### Non-Chemical Drug""")
        st.write("This is an Antibody")
    else:
        # Display drug information
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
            
        st.markdown("### Similar Structures")
        st.table(return_similar(drug))

elif tab == "Download":
    # Display logo and subheader for the Download tab
    display_logo()
    st.subheader("DOWNLOAD")
    
    # Create a dropdown to select cancer type for download
    cancers_list = [part + " Cancer" for part in ["Breast", "Ovarian", "Pancreatic", "Prostate"]]
    cancer_type = st.selectbox("Select Cancer Type", cancers_list, key="sourceKey")
    option = cancer_type.split()[0].lower()
    
    # Construct the URL for the selected cancer type
    url = "https://www.cancer.gov/about-cancer/treatment/drugs/" + option
    
    # Get a list of approved drugs for the selected cancer type
    approved_drugs_list = return_approved(url)
    
    # Create an empty DataFrame to store the final CSV data
    final_csv = pd.DataFrame()
    
    # Display progress bar and iterate through drugs to create CSV
    latest_iteration = st.empty()
    bar = st.progress(0)
    count = 1
    
    for i in range(len(approved_drugs_list)):
        latest_iteration.text(f'Drug {count} of {len(approved_drugs_list)}')
        value = int(count / len(approved_drugs_list) * 100)
        bar.progress(value)
        
        drug = approved_drugs_list[i]
        drug_csv = return_similar(drug)
        drug_csv = drug_csv[drug_csv["Attempted with Cancer"]]
        final_csv.append(drug_csv)
        
        count += 1
    
    # Display the final CSV table
    st.table(final_csv)
    
    # Convert CSV to bytes for download
    analogous_csv = final_csv.to_csv().encode('utf-8')
    
    # Display download button
    st.write("\n\n\n")
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col4:
        st.download_button('Download CSV', data=analogous_csv, file_name=option+"-analogs.csv", mime='text/csv')
