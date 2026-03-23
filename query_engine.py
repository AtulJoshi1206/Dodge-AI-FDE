import streamlit as st
import re

def get_node(G, node_type, node_id):
    """Find node: NodeType_ID"""
    full_id = f"{node_type}_{node_id}"
    if G.has_node(full_id):
        return full_id
    return None

def get_neighbors_by_relation(G, node, relation, direction="out"):
    """
    Find neighbors connected by a specific relation attribute.
    direction: "out" (successors) or "in" (predecessors)
    """
    neighbors = []
    if direction == "out":
        for n in G.successors(node):
            if G[node][n].get("relation") == relation:
                neighbors.append(n)
    else:  # direction == "in"
        for n in G.predecessors(node):
            if G[n][node].get("relation") == relation:
                neighbors.append(n)
    return neighbors

def get_all_nodes_by_type(G, node_type):
    """Iterate all nodes of a specific type label"""
    return [n for n, attr in G.nodes(data=True) if attr.get("type_label") == node_type]

@st.cache_data(show_spinner=False)
def execute_query(user_query: str, _G):
    # Rename for internal use
    G = _G
    user_query = user_query.strip().lower()
    
    # 1. "orders by customer <ID>"
    match1 = re.match(r"orders by customer (\w+)", user_query)
    if match1:
        cust_id = match1.group(1)
        node = get_node(G, "Customer", cust_id)
        if not node:
            return {"intent": "orders_by_customer", "status": "error", "message": f"Customer {cust_id} not found", "count": 0, "data": []}
        
        # In GRAPH_SCHEMA: SalesOrder -> Customer (placed_by). So SalesOrder is predecessor.
        orders = get_neighbors_by_relation(G, node, "placed_by", direction="in")
        return {"intent": "orders_by_customer", "status": "success", "count": len(orders), "data": orders}

    # 2. "products in order <ID>"
    match2 = re.match(r"products in order (\w+)", user_query)
    if match2:
        order_id = match2.group(1)
        node = get_node(G, "SalesOrder", order_id)
        if not node:
            return {"intent": "products_in_order", "status": "error", "message": f"Order {order_id} not found", "count": 0, "data": []}
        
        # Chain: Product <- orders_product - SalesOrderItem - belongs_to -> SalesOrder
        # Step A: Find SalesOrderItems (Inwards 'belongs_to' to SalesOrder)
        items = get_neighbors_by_relation(G, node, "belongs_to", direction="in")
        
        # Step B: Find Products (Outwards 'orders_product' from Items)
        products = []
        for item in items:
            prods = get_neighbors_by_relation(G, item, "orders_product", direction="out")
            products.extend(prods)
            
        unique_products = list(set(products))
        return {"intent": "products_in_order", "status": "success", "count": len(unique_products), "data": unique_products}

    # 3. "orders without delivery"
    if user_query == "orders without delivery":
        orders = get_all_nodes_by_type(G, "SalesOrder")
        missing_delivery = []
        for o in orders:
            # Relation: Delivery - fulfills -> SalesOrder. So Delivery is predecessor.
            fulfillments = get_neighbors_by_relation(G, o, "fulfills", direction="in")
            if not fulfillments:
                missing_delivery.append(o)
        return {"intent": "orders_without_delivery", "status": "success", "count": len(missing_delivery), "data": missing_delivery}

    # 4. "invoices without payment"
    if user_query == "invoices without payment":
        invoices = get_all_nodes_by_type(G, "Invoice")
        unpaid = []
        for i in invoices:
            # Relation: Payment - clears -> Invoice. So Payment is predecessor.
            payments = get_neighbors_by_relation(G, i, "clears", direction="in")
            if not payments:
                unpaid.append(i)
        return {"intent": "invoices_without_payment", "status": "success", "count": len(unpaid), "data": unpaid}

    return {"intent": "unknown", "status": "error", "message": "unsupported query", "count": 0, "data": []}

if __name__ == "__main__":
    # Test cases
    print("Test 1: orders by customer 310000108")
    print(execute_query("orders by customer 310000108"))
    
    print("\nTest 2: products in order 740506")
    print(execute_query("products in order 740506"))
    
    print("\nTest 3: orders without delivery")
    res3 = execute_query("orders without delivery")
    print(f"Count: {res3['count']}")
    
    print("\nTest 4: invoices without payment")
    res4 = execute_query("invoices without payment")
    print(f"Count: {res4['count']}")
