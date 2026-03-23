import os
import json
import pandas as pd
import networkx as nx
from schema import SCHEMA
from graph_schema import GRAPH_SCHEMA

DATA_DIR = os.path.join(os.path.dirname(__file__), "sap-o2c-data")

NODE_TABLE_MAP = {
    "Customer": {"table": "business_partners", "id_cols": ["customer"]},
    "SalesOrder": {"table": "sales_order_headers", "id_cols": ["salesOrder"]},
    "SalesOrderItem": {"table": "sales_order_items", "id_cols": ["salesOrder", "salesOrderItem"]},
    "Product": {"table": "products", "id_cols": ["product"]},
    "Delivery": {"table": "outbound_delivery_headers", "id_cols": ["deliveryDocument"]},
    "Invoice": {"table": "billing_document_headers", "id_cols": ["billingDocument"]},
    "Payment": {"table": "payments_accounts_receivable", "id_cols": ["accountingDocument"]},
    "Plant": {"table": "plants", "id_cols": ["plant"]}
}

def load_data():
    dfs = {}
    for table_name in os.listdir(DATA_DIR):
        table_path = os.path.join(DATA_DIR, table_name)
        if os.path.isdir(table_path):
            files = [os.path.join(table_path, f) for f in os.listdir(table_path) if f.endswith('.jsonl')]
            if files:
                dfs[table_name] = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
            else:
                dfs[table_name] = pd.DataFrame()
    return dfs

def make_id(row, cols, prefix):
    try:
        if any(pd.isna(row[c]) for c in cols):
            return None
        # Handle floats cleanly to avoid IDs like "Delivery_740506.0"
        vals = [str(int(row[c])) if isinstance(row[c], float) and row[c].is_integer() else str(row[c]) for c in cols]
        return f"{prefix}_" + "_".join(vals)
    except:
        return None

def build_graph():
    dfs = load_data()
    G = nx.DiGraph()

    # 1. Create Nodes
    for node_type, config in NODE_TABLE_MAP.items():
        table = config["table"]
        id_cols = config["id_cols"]
        if table in dfs and not dfs[table].empty:
            df = dfs[table]
            for _, row in df.iterrows():
                node_id = make_id(row, id_cols, node_type)
                if node_id:
                    # Clean row for attributes (remove NaNs)
                    attrs = {k: v for k, v in row.to_dict().items() if pd.notna(v)}
                    G.add_node(node_id, type_label=node_type, **attrs)

    # 2. Create Edges
    for edge in GRAPH_SCHEMA["edges"]:
        from_type = edge["from"]
        to_type = edge["to"]
        rel = edge["relation"]
        src_table = edge["source_table"]
        tgt_table = edge["target_table"]
        join_cond = edge["join_condition"]

        left_part, right_part = join_cond.split("==")
        col1 = left_part.strip().split(".")[1]
        col2 = right_part.strip().split(".")[1]

        if src_table not in dfs or tgt_table not in dfs:
            continue
            
        df_A = dfs[src_table].copy()
        df_B = dfs[tgt_table].copy()

        if df_A.empty or df_B.empty:
            continue

        if col1 not in df_A.columns or col2 not in df_B.columns:
            continue

        id_cols_A = NODE_TABLE_MAP[from_type]["id_cols"]
        id_cols_B = NODE_TABLE_MAP[to_type]["id_cols"]

        if not all(c in df_A.columns for c in id_cols_A):
            continue
        if not all(c in df_B.columns for c in id_cols_B):
            continue

        # Generate Node IDs safely
        df_A['_from_node_id'] = df_A.apply(lambda r: make_id(r, id_cols_A, from_type), axis=1)
        df_B['_to_node_id'] = df_B.apply(lambda r: make_id(r, id_cols_B, to_type), axis=1)

        # Drop rows where we couldn't generate a node ID
        df_A_sub = df_A[['_from_node_id', col1]].dropna()
        df_B_sub = df_B[['_to_node_id', col2]].dropna()

        # Perform the relational Join
        merged = pd.merge(df_A_sub, df_B_sub, left_on=col1, right_on=col2)
        
        seen_edges = set()
        for _, row in merged.iterrows():
            u = row['_from_node_id']
            v = row['_to_node_id']
            if pd.notna(u) and pd.notna(v):
                # Ensure edges only link existing nodes
                if G.has_node(u) and G.has_node(v):
                    edge_key = (u, v, rel)
                    if edge_key not in seen_edges:
                        G.add_edge(u, v, relation=rel)
                        seen_edges.add(edge_key)

    return G

if __name__ == "__main__":
    g = build_graph()
    print(f"Graph Construction Complete! Loaded {g.number_of_nodes()} nodes and {g.number_of_edges()} edges.")
