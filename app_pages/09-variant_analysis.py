import streamlit as st
import pm4py
from pm4py.objects.conversion.ocel.variants import ocel_features_to_nx, ocel_to_nx
import networkx as nx
import matplotlib.pyplot as plt

# Set the title of the app
st.title("OCEL Variants Analysis and Visualization")

# Check if OCEL object is available in session state
if 'ocel' not in st.session_state:
    st.warning("Please upload an OCEL event log first on the Upload page.")
else:
    # Load the OCEL object from session state
    ocel = st.session_state['ocel']

    # Sidebar for selecting which graphs to include
    st.sidebar.title("Select Graphs to Include")
    include_obj_interaction_graph = st.sidebar.checkbox("Include Object Interaction Graph")
    include_obj_descendants_graph = st.sidebar.checkbox("Include Object Descendants Graph")
    include_obj_inheritance_graph = st.sidebar.checkbox("Include Object Inheritance Graph")
    include_obj_cobirth_graph = st.sidebar.checkbox("Include Object Cobirth Graph")
    include_obj_codeath_graph = st.sidebar.checkbox("Include Object Codeath Graph")
    include_df = st.sidebar.checkbox("Include Directly-Follows Relationship")
    include_object_changes = st.sidebar.checkbox("Include Object Changes")

    # Define parameters for the conversion functions
    parameters_features = {
        ocel_features_to_nx.Parameters.INCLUDE_OBJ_INTERACTION_GRAPH: include_obj_interaction_graph,
        ocel_features_to_nx.Parameters.INCLUDE_OBJ_DESCENDANTS_GRAPH: include_obj_descendants_graph,
        ocel_features_to_nx.Parameters.INCLUDE_OBJ_INHERITANCE_GRAPH: include_obj_inheritance_graph,
        ocel_features_to_nx.Parameters.INCLUDE_OBJ_COBIRTH_GRAPH: include_obj_cobirth_graph,
        ocel_features_to_nx.Parameters.INCLUDE_OBJ_CODEATH_GRAPH: include_obj_codeath_graph
    }

    parameters_nx = {
        ocel_to_nx.Parameters.INCLUDE_DF: include_df,
        ocel_to_nx.Parameters.INCLUDE_OBJECT_CHANGES: include_object_changes
    }

    # Apply the conversion to obtain NetworkX graphs
    G_features = ocel_features_to_nx.apply(ocel, parameters_features)
    G_nx = ocel_to_nx.apply(ocel, parameters_nx)

    # Visualize the graphs
    def draw_graph(graph, title):
        plt.figure(figsize=(10, 7))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=500, font_size=10)
        plt.title(title)
        st.pyplot(plt)

    # Display the graphs based on selected options
    st.header("Graph Visualizations")
    if include_obj_interaction_graph:
        st.subheader("Object Interaction Graph")
        draw_graph(G_features, "Object Interaction Graph")

    if include_obj_descendants_graph:
        st.subheader("Object Descendants Graph")
        draw_graph(G_features, "Object Descendants Graph")

    if include_obj_inheritance_graph:
        st.subheader("Object Inheritance Graph")
        draw_graph(G_features, "Object Inheritance Graph")

    if include_obj_cobirth_graph:
        st.subheader("Object Cobirth Graph")
        draw_graph(G_features, "Object Cobirth Graph")

    if include_obj_codeath_graph:
        st.subheader("Object Codeath Graph")
        draw_graph(G_features, "Object Codeath Graph")

    if include_df:
        st.subheader("Directly-Follows Relationship Graph")
        draw_graph(G_nx, "Directly-Follows Relationship Graph")

    if include_object_changes:
        st.subheader("Object Changes Graph")
        draw_graph(G_nx, "Object Changes Graph")

    # Display a message if no options are selected
    if not any([include_obj_interaction_graph, include_obj_descendants_graph, include_obj_inheritance_graph, include_obj_cobirth_graph, include_obj_codeath_graph, include_df, include_object_changes]):
        st.write("Please select at least one graph to include from the sidebar.")