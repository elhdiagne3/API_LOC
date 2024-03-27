#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import saspy

def filter_elements(callermsisdns):

    sas = saspy.SASsession(cfgname='httpsviya')
    
    for callermsisdn in callermsisdns:

        sas.submit(f'''
            proc sql;
                create table dfra.localisation_switch_rest as
                select *
                from dfra.localisation_switch_
                where callermsisdn = '{callermsisdn}';
            quit;
        ''')
        st.write(f'Table filtrée pour callermsisdn {callermsisdn} envoyée vers SAS Visual Analytics')
    sas.submit('''
                /*****************************************************************************/
                /*  Start a session named mySession using the existing CAS server connection */
                /*  while allowing override of caslib, timeout (in seconds), and locale     */
                /*  defaults.                                                                */
                /*****************************************************************************/
                options cashost="bigdviyaccont1.orangemali.local" casport=5580;
                cas myCTsession sessopts=(caslib=casuser timeout=1800 locale="en_US");
                cas myCTsession list; 
                /*---------------------------------------------------------------------------------*/
                /*     Make all the defined (global) SAS Libraries available for this session      */
                /*---------------------------------------------------------------------------------*/
                caslib _all_ assign; 
                
                proc casutil incaslib="reportdfra" outcaslib="reportdfra";
                    droptable casdata="localisation_switch_rest" quiet;
                    load data=dfra.localisation_switch_rest casout="localisation_switch_rest" promote;
                    save casdata="localisation_switch_rest" replace;
                run;
    ''')

    # Affiche le lien vers SAS Visual Analytics
    st.write("Votre table filtrée a été envoyée vers SAS Visual Analytics.")
    st.write("Vous pouvez accéder au rapport ici :")
    url = "https://bigdataviya.orangemali.local/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F961b1c48-34ec-4d35-844c-097458c739e2&sectionIndex=0&objectName=vi95&quickView=true&sas-welcome=false"
    st.markdown(f"[Lien vers SAS Visual Analytics]({url})")

def main():
    st.title('API LOCALISATION SWITCH')
                    
    callermsisdns_input = st.text_input('Veuiller selectionner le msisdn à filtrer:')
            
    if st.button('Filtrer'):
        callermsisdns = callermsisdns_input.split(',')
        filter_elements(callermsisdns)

if __name__ == '__main__':
    main()

