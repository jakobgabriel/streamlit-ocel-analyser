import streamlit as st

# Define Page Navigation and Pages
pages = {
    "Home" : [
        st.Page("app_pages/home/00-home.py", title="Home", icon=":material/home:") #TODO
    ],
    "Upload" : [
        st.Page("app_pages/upload/upload.py", title="Upload Event Log", icon=":material/upload:")
    ],
    "OCEL - Summary Statistics" : [
        st.Page("app_pages/summary/log_overview.py", title="Event Log Summary", icon=":material/summarize:")
    ],
    "OCEL - Objects and Object Types" : [
        st.Page("app_pages/ocel/objects/03-object_types.py", title="Object Types", icon=":material/category:"),
        st.Page("app_pages/ocel/objects/04-objects.py", title="Objects", icon=":material/widgets:"), #TODO
    ],
    "OCEL - Events and Event Types" : [
        st.Page("app_pages/ocel/events/05-event_types.py", title="Event Types", icon=":material/event:"), #TODO
        st.Page("app_pages/ocel/events/06-events.py", title="Events", icon=":material/event_list:"), #TODO
    ],
    "OCEL - Other Visualizations" : [
        st.Page("app_pages/ocel/visualization/07-relationships.py", title="Event Object Relationships", icon=":material/merge_type:"),
        st.Page("app_pages/ocel/visualization/08-interactions.py", title="Object Interactions", icon=":material/family_history:"), # TODO
        st.Page("app_pages/ocel/visualization/09-variant_analysis.py", title="Variant Analysis", icon=":material/variable_insert:")
    ],
    "OCEL - Process Discovery" : [
        st.Page("app_pages/ocel/process_discovery/process_discovery_ocdfg.py", title="Object Centric Direct Follows Graph", icon=":material/hub:"),
        st.Page("app_pages/ocel/process_discovery/process_discovery_ocpn.py", title="Object Centric Petri Net", icon=":material/hub:"),
    ],
    "OCEL x LLM": [
        st.Page("app_pages/ocel/llm/ocel_log_abstraction.py", title="OCEL Log Abstraction", icon=":material/neurology:"),
        #st.Page("app_pages/ocel/llm/feature_abstraction.py", title="OCEL Feature Abstraction", icon=":material/neurology:"), #TODO
        st.Page("app_pages/ocel/llm/ocdfg_abstraction.py", title="OC-DFG Abstraction", icon=":material/draw_abstract:")
    ],
    "OCEL Flattening to XES" : [
        st.Page("app_pages/xes/conversion/01-event_flattening.py", title="Event Log Flattening", icon=":material/iron:")
    ], 
    "XES - Visualization": [
        st.Page("app_pages/xes/visualization/01-dotted_chart.py", title="Dotted Chart", icon=":material/scatter_plot:"),
        st.Page("app_pages/xes/visualization/01-variants_plot.py", title="Variants Chart", icon=":material/key_visualizer:"),
        st.Page("app_pages/xes/visualization/02-process_tree.py", title="Process Tree", icon=":material/account_tree:"),
        st.Page("app_pages/xes/visualization/03-case_duration_graph.py", title="Case Duration Graph", icon=":material/progress_activity:"),
        st.Page("app_pages/xes/visualization/04-event_distribution_graph.py", title="Event Distribution Graph", icon=":material/horizontal_distribute:"),
        st.Page("app_pages/xes/visualization/05-performance_spectrum.py", title="Performance Spectrum", icon=":material/key_visualizer:")
    ],
    "XES x LLM" : [
        st.Page("app_pages/xes/llm/variants_abstraction.py", title="Variants Abstraction", icon=":material/neurology:"),
        st.Page("app_pages/xes/llm/dfg_abstraction.py", title="DFG Abstraction", icon=":material/draw_abstract:")
    ]
}

# Build Page Navigation
pg = st.navigation(pages)
pg.run()