import streamlit as st

# Define Page Navigation and Pages
pages = {
    "Home" : [
        st.Page("app_pages/00-home.py", title="Home", icon=":material/home:") #TODO
    ],
    "Upload" : [
        st.Page("app_pages/01-upload.py", title="Upload Event Log", icon=":material/upload:")
    ],
    "Statistics" : [
        st.Page("app_pages/02-log_overview.py", title="Event Log Summary", icon=":material/summarize:"),
        st.Page("app_pages/03-object_types.py", title="Object Types", icon=":material/category:"),
        st.Page("app_pages/04-objects.py", title="Objects", icon=":material/widgets:"), #TODO
        st.Page("app_pages/05-event_types.py", title="Event Types", icon=":material/event:"), #TODO
        st.Page("app_pages/06-events.py", title="Events", icon=":material/event_list:"), #TODO
        st.Page("app_pages/07-relationships.py", title="Event Object Relationships", icon=":material/merge_type:"),
        st.Page("app_pages/08-interactions.py", title="Object Interactions", icon=":material/family_history:"), # TODO
        st.Page("app_pages/09-variant_analysis.py", title="Test")
    ], 
    "Process Discovery" : [
        st.Page("app_pages/20-process_discovery_ocdfg.py", title="Object Centric Direct Follows Graph", icon=":material/hub:"), #TODO
        st.Page("app_pages/21-process_discovery_ocpn.py", title="Object Centric Petri Net", icon=":material/hub:"), #TODO
    ]
}

# Build Page Navigation
pg = st.navigation(pages)
pg.run()