#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import saspy

# Function to filter elements
def filter_elements(callermsisdns):
    # Connect to SAS session
    sas = saspy.SASsession(cfgname='httpsviya')
    
    for callermsisdn in callermsisdns:
        # Execute SAS query to filter data
        sas.submit(f'''
            proc sql;
                create table dfra.localisation_switch_rest as
                select *
                from dfra.localisation_switch_
                where callermsisdn = '{callermsisdn}';
            quit;
        ''')

        # Display message for each filtered element
        st.write(f'Table filtrée pour callermsisdn {callermsisdn} envoyée vers SAS Visual Analytics')

    # Additional SAS processing (if any)
    sas.submit('''
        proc casutil incaslib="reportdfra" outcaslib="reportdfra";
            droptable casdata="localisation_switch_rest" quiet;
            load data=dfra.localisation_switch_rest casout="localisation_switch_rest" promote;
            save casdata="localisation_switch_rest" replace;
        run;
    ''')

    # Display link to SAS Visual Analytics
    st.write("Votre table filtrée a été envoyée vers SAS Visual Analytics.")
    st.write("Vous pouvez accéder au rapport ici :")
    url = "https://bigdataviya.orangemali.local/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F961b1c48-34ec-4d35-844c-097458c739e2&sectionIndex=0&objectName=vi95&quickView=true&sas-welcome=false"
    st.markdown(f"[Lien vers SAS Visual Analytics]({url})")

# Main function to create Streamlit app
def main():
    st.title('API LOCALISATION SWITCH')
                    
    # Input field for callermsisdns
    callermsisdns_input = st.text_input('Veuillez sélectionner le msisdn à filtrer:')
            
    # Button to trigger filtering
    if st.button('Filtrer'):
        callermsisdns = callermsisdns_input.split(',')
        filter_elements(callermsisdns)

# Entry point of the Streamlit app
if __name__ == '__main__':
    main()

