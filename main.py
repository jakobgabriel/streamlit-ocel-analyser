import streamlit as st

# Define Page Navigation and Pages
pages = {
    "Home" : [
        st.Page("pages/00-home.py", title="Home", icon=":material/home:") #TODO
    ],
    "Upload" : [
        st.Page("pages/01-upload.py", title="Upload Event Log", icon=":material/upload:")
    ],
    "Statistics" : [
        st.Page("pages/02-log_overview.py", title="Event Log Summary", icon=":material/summarize:"),
        st.Page("pages/03-object_types.py", title="Object Types", icon=":material/category:"),
        st.Page("pages/04-objects.py", title="Objects", icon=":material/widgets:"), #TODO
        st.Page("pages/05-event_types.py", title="Event Types", icon=":material/event:"), #TODO
        st.Page("pages/06-events.py", title="Events", icon=":material/event_list:"), #TODO
        st.Page("pages/07-relationships.py", title="Event Object Relationships", icon=":material/merge_type:"),
        st.Page("pages/08-interactions.py", title="Object Interactions", icon=":material/family_history:") # TODO
    ], 
    "Process Discovery" : [
        #st.Page("pages/04-event_types.py", title="Event Type Overview", icon=":material/hub:"), #TODO
    ]
}

# Build Page Navigation
pg = st.navigation(pages)
pg.run()