import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
from pyvis.network import Network
from dotenv import load_dotenv

# Load Environment Variables (.env)
load_dotenv()

# Import backend logic
from graph_builder import build_graph
from llm_router import route_query

# Page Config
st.set_page_config(page_title="SAP O2C Graph Explorer", layout="wide")

st.title("🕸️ Graph-Based O2C Query System")
st.markdown("---")

# 1. Cache Graph Generation
@st.cache_resource
def get_cached_graph():
    return build_graph()

G = get_cached_graph()

# 2. State Management for Results
if 'query_result' not in st.session_state:
    st.session_state.query_result = None

# Layout
left_col, right_col = st.columns([1, 2])

# --- LEFT PANEL: QUERY INTERFACE ---
with left_col:
    st.subheader("Query Interface")
    user_input = st.text_input("Ask a question about Order-to-Cash data:", 
                               placeholder="e.g., orders by customer 310000108")
    
    if st.button("Run Query", use_container_width=True):
        if not os.environ.get("GOOGLE_API_KEY"):
            st.error("Missing GOOGLE_API_KEY. Please set it in your .env file.")
        elif user_input:
            with st.spinner("Routing query via LLM..."):
                result = route_query(user_input)
                st.session_state.query_result = result
        else:
            st.warning("Please enter a query.")

    if st.session_state.query_result:
        res = st.session_state.query_result
        
        if res["status"] == "rejected":
            st.warning(f"⚠️ Query Rejected: {res.get('reason', 'Unsupported domain')}")
            if "mapped_query" in res:
                st.caption(f"LLM Mapped to: {res['mapped_query']}")
        elif res["status"] == "success":
            st.success("Query Executed Successfully")
            st.info(f"**Intent:** {res['mapped_query']}")
            
            data = res["data"]
            st.metric("Results Found", data["count"])
            
            with st.expander("View Raw Data", expanded=True):
                st.json(data["data"])
        else:
            st.error(f"Error: {res.get('reason', 'Unknown error')}")

# --- RIGHT PANEL: GRAPH VISUALIZATION ---
with right_col:
    st.subheader("Interactive Graph Visualization")
    
    # Check if a query was run and if it has zero results
    has_active_query = st.session_state.query_result is not None and st.session_state.query_result["status"] == "success"
    query_count = st.session_state.query_result["data"]["count"] if has_active_query else -1
    
    if has_active_query and query_count == 0:
        st.warning("🔍 No results found for this query. The graph will not be rendered to avoid misleading visualization.")
        st.image("https://img.icons8.com/isometric/512/empty-box.png", width=200) # Optional visual placeholder
    else:
        # Visualization Logic
        def generate_viz(highlight_nodes=None):
            net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black", directed=True)
            
            # Determine the set of nodes to include in the visualization
            if highlight_nodes:
                # Subgraph: result nodes + their 1-hop neighbors
                nodes_to_include = set(highlight_nodes)
                for n in highlight_nodes:
                    if G.has_node(n):
                        nodes_to_include.update(G.successors(n))
                        nodes_to_include.update(G.predecessors(n))
                subgraph_nodes = nodes_to_include
            else:
                # Fallback: show everything (standard behavior for no active query)
                subgraph_nodes = G.nodes()

            # Build visual components for the specified nodes
            for node in subgraph_nodes:
                if not G.has_node(node): continue
                attrs = G.nodes[node]
                node_type = attrs.get("type_label", "Unknown")
                label = f"{node}"
                
                # Dynamic Styling
                if highlight_nodes and node in highlight_nodes:
                    color = "#ff4b4b" # Result Nodes: RED
                    size = 35
                elif highlight_nodes:
                    color = "#ffa500" # 1-hop Neighbors: ORANGE
                    size = 20
                else:
                    color = "#97c2fc" # Default View: BLUE
                    size = 20
                    
                net.add_node(node, label=label, title=f"Type: {node_type}", color=color, size=size)
                
            # Add edges only if both endpoints are in the subgraph
            for u, v, attrs in G.edges(data=True):
                if u in subgraph_nodes and v in subgraph_nodes:
                    net.add_edge(u, v, label=attrs.get("relation", ""))
                
            # Physics and interactivity
            net.toggle_physics(True)
            net.set_options("""
            var options = {
              "physics": {
                "forceAtlas2Based": {
                  "gravitationalConstant": -50,
                  "centralGravity": 0.01,
                  "springLength": 100,
                  "springConstant": 0.08
                },
                "maxVelocity": 50,
                "solver": "forceAtlas2Based",
                "timestep": 0.35,
                "stabilization": {"enabled": true, "iterations": 100}
              }
            }
            """)
            
            # Save and return HTML
            temp_file = "graph_output.html"
            net.write_html(temp_file)
            with open(temp_file, 'r', encoding='utf-8') as f:
                return f.read()

        # Determine nodes to highlight
        highlight_list = []
        if has_active_query:
            highlight_list = st.session_state.query_result["data"]["data"]
            
        html_content = generate_viz(highlight_list if has_active_query else None)
        components.html(html_content, height=650)
        
        st.caption("Hold 'Ctrl' and scroll to zoom. Click and drag nodes to explore.")

