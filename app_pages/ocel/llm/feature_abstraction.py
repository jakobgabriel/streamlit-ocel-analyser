import streamlit as st
import pm4py

# Set the page configuration to wide
st.set_page_config(page_title="OCEL Features Abstraction", layout="wide")

# Function to obtain the OCEL features abstraction
def get_ocel_features_abstraction():
    st.title('OCEL Features Abstraction')
    if 'ocel' not in st.session_state:
        st.warning("No object-centric event log available. Please upload or generate an object-centric event log first.")
    else:
        ocel = st.session_state['ocel']
        
        st.sidebar.header("OCEL Features Abstraction Settings")
        
        # Get the available object types
        try:
            object_types = pm4py.ocel_get_object_types(ocel)
        except Exception as e:
            st.error(f"Error obtaining object types: {e}")
            return
        
        obj_type = st.sidebar.selectbox("Object Type", options=object_types)
        include_header = st.sidebar.checkbox("Include Header", value=True)
        max_len = st.sidebar.number_input("Maximum Length", min_value=1, value=10000)
        debug = st.sidebar.checkbox("Enable Debugging Mode", value=False)
        enable_object_lifecycle_paths = st.sidebar.checkbox("Enable Object Lifecycle Paths", value=True)
        
        if st.sidebar.button("Generate OCEL Features Abstraction"):
            try:
                ocel_features_abstraction = pm4py.llm.abstract_ocel_features(
                    ocel=ocel,
                    obj_type=obj_type,
                    include_header=include_header,
                    max_len=max_len,
                    debug=debug,
                    enable_object_lifecycle_paths=enable_object_lifecycle_paths
                )
                st.subheader("OCEL Features Abstraction Result")
                st.text_area("Abstraction", value=ocel_features_abstraction, height=500)
            except Exception as e:
                st.error(f"Error generating OCEL features abstraction: {e}")

# Streamlit page structure
if 'ocel' not in st.session_state:
    st.warning("Please upload an object-centric event log first on the Upload page.")
else:
    st.title("Object-Centric Event Log Features Abstraction")
    get_ocel_features_abstraction()