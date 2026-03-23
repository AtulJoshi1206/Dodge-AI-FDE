# Session Prompt History: SAP O2C Graph Query System

## Phase 1: Schema Extraction

### Prompt 1
We are building a Graph-Based Data Modeling and Query System for SAP Order-to-Cash data.

Goal:
- Convert CSV dataset into structured entities and relationships
- Prepare for graph construction (Neo4j or NetworkX later)

Current Task:
Step 1: Analyze dataset structure ONLY (no graph yet)

Dataset Path:
"/Users/atuljoshi/Documents/Projects/Dodge AI/sap-o2c-data"

Instructions:
1. Read all CSV files in the folder
2. For each file:
   - Identify primary key
   - Identify possible foreign keys
   - List all columns
3. Infer relationships between tables (based on column names like *_id)
4. Output a structured schema in Python dictionary format like:

{
  "orders": {
    "primary_key": "order_id",
    "foreign_keys": ["customer_id"],
    "columns": [...]
  }
}

Constraints:
- DO NOT assume anything not present in data
- DO NOT build graph yet
- DO NOT use any external APIs
- Keep logic modular and clean

Output:
- Save result in schema.py as a dictionary named SCHEMA

Context: Initial analysis of the raw O2C dataset to infer relational structure.

### Outcome
- **Built**: `analyze.py` script and `schema.py` containing inferred structure of 19+ tables.
- **Issue**: Found data was in JSONL format, not CSV as initially assumed.
- **Fix**: Updated `analyze.py` to use `json.loads()` and `pandas.read_json()`.
- **Result**: Structured schema dictionary ready for graph mapping.

---

## Phase 2: Graph Schema Design

### Prompt 2
We have already extracted dataset schema in SCHEMA dictionary.

Now we want to design a CLEAN graph model for SAP Order-to-Cash business flow.

OBJECTIVE:
Convert raw relational schema into a simplified, high-signal graph schema for downstream query execution.

---

TASK:

1. Map raw tables into simplified graph nodes:

   - Customer
   - SalesOrder
   - SalesOrderItem
   - Product
   - Delivery (DeliveryHeader + DeliveryItem)
   - Invoice (BillingHeader + BillingItem)
   - Payment (PaymentsAccountsReceivable / Journal Entries)
   - Plant

2. Define directed relationships (edges) between nodes.

Each edge MUST include:
- from (node)
- to (node)
- relation (semantic name)
- source_table
- target_table
- join_condition (explicit, correct, executable)

---

CRITICAL SAP-SPECIFIC HINTS:

- Product is referred to as `material`
- Customer is referred to as `soldToParty` or `customer`
- Sales Order ID = `salesOrder`
- Delivery ID = `deliveryDocument`
- Invoice ID = `billingDocument`
- Payment link via `accountingDocument`

---

CONSTRAINTS:

- Keep it simple (one node per entity type)
- Direction: Flow of business (Order -> Delivery -> Invoice -> Payment)
- Use standard Python typing
- Output: Store result in graph_schema.py as dictionary named GRAPH_SCHEMA

Context: Mapping relational tables to semantic graph entities and defining directional edges.

### Outcome
- **Built**: `graph_schema.py` defining 8 node types and 10+ directional relationships.
- **Issue**: Ambiguity between `billingDocument` and `accountingDocument` column names.
- **Fix**: Applied specialized SAP O2C heuristics to explicitly map join conditions.
- **Result**: Validated graph schema ensuring flow from Order to Payment.

---

## Phase 3: Graph Construction

### Prompt 3
We have GRAPH_SCHEMA and SCHEMA ready.

Now build the graph construction pipeline.

OBJECTIVE:
Convert dataset into an actual graph using NetworkX.

---

TASK:

1. Create file: graph_builder.py

2. Load all dataset files from:
"/Users/atuljoshi/Documents/Projects/Dodge AI/sap-o2c-data"

3. For each node type:
- Create nodes with unique IDs
- Attach relevant attributes

4. For each edge in GRAPH_SCHEMA:
- Perform join using join_condition
- Create edges between nodes

5. Use NetworkX DiGraph

---

REQUIREMENTS:

- Use pandas for data loading
- Handle missing values safely
- Avoid duplicate nodes
- Ensure edge creation only if both nodes exist
- Keep code modular

---

OUTPUT:

Function:

def build_graph():
    return graph

Graph should contain:
- Nodes with type labels
- Edges with relation labels

---

DO NOT:
- Use any LLM
- Build UI
- Add extra features

ONLY build graph from schema

Context: Implementing the actual graph building logic using NetworkX and Pandas.

### Outcome
- **Built**: `graph_builder.py` pipeline using NetworkX DiGraph.
- **Issue**: Missing `networkx` library causing script failure during execution.
- **Fix**: Installed dependency via `pip3 install networkx`.
- **Final Result**: Successfully constructed graph with **757 nodes** and **1253 edges**.

---

## Phase 4: Query Engine

### Prompt 4
We now have a fully built NetworkX graph using build_graph().

We will build a deterministic Query Engine that maps controlled natural language patterns to graph traversal logic.

---

OBJECTIVE:
Create file: query_engine.py

---

SETUP:

from graph_builder import build_graph
import re

G = build_graph()

---

TASK:

Define:

def execute_query(user_query: str):
    """
    Takes a natural language query string and returns structured result from graph
    """

---

SUPPORTED INTENTS (STRICT MATCH ONLY):

1. "orders by customer <ID>"
2. "products in order <ID>"
3. "orders without delivery"
4. "invoices without payment"

---

IMPLEMENTATION DETAILS:

### Helper functions (MANDATORY):

- get_node(node_type, node_id)
- get_neighbors_by_relation(node, relation, direction="out")
- get_all_nodes_by_type(node_type)

---

### Intent 1:
"orders by customer <ID>"

- Find node: Customer_<ID>
- Traverse incoming edges with relation = "placed_by"
- Return SalesOrder nodes

---

### Intent 2:
"products in order <ID>"

- Find node: SalesOrder_<ID>
- Traverse:
  SalesOrder → SalesOrderItem → Product
- Use relation chain: belongs_to + orders_product
- Return Product nodes

---

### Intent 3 (BROKEN FLOW):
"orders without delivery"

- Iterate all SalesOrder nodes
- Check if ANY outgoing edge with relation = "fulfilled_by" exists
- If not → add to result

---

### Intent 4 (BROKEN FLOW):
"invoices without payment"

- Iterate all Invoice nodes
- Check if ANY incoming edge with relation = "clears" exists
- If not → add to result

---

RESULT FORMAT:

Return:

{
  "intent": "<intent_name>",
  "status": "success" | "error",
  "count": <number>,
  "data": [list of node IDs]
}

---

ERROR HANDLING:

- If node not found → return status = "error"
- If invalid query → return "unsupported query"

---

CONSTRAINTS:

- Node format: NodeType_ID (e.g., Customer_310000108)
- Use graph[node] and graph.predecessors()/successors()
- Use edge attribute: relation
- NO LLM usage
- NO external APIs

---

VALIDATION:

Test queries:
- "orders by customer 310000108"
- "products in order <valid_order_id>"
- "orders without delivery"
- "invoices without payment"

Ensure correct outputs before finishing.

---

GOAL:

Build a deterministic, testable, and explainable query layer over the graph.

Context: Creating a hardcoded traversal layer for zero-hallucination data extraction.

### Outcome
- **Built**: `query_engine.py` with `execute_query` supporting 4 core business intents.
- **Issue**: Reverse document flow logic (Traversing from Child to Parent) was initially complex.
- **Fix**: Implemented `get_neighbors_by_relation` to handle both `in`/`out` directions.
- **Result**: High-speed, data-backed query layer for SAP data.

---

## Phase 5: LLM Router

### Prompt 5
We have a deterministic query engine (execute_query) that works perfectly.

Now we will build an LLM Router that strictly maps user queries to supported intents.

---

OBJECTIVE:
Create file: llm_router.py

---

SETUP:

- Use a free LLM API (Groq Llama3 preferred OR Gemini)
- Keep API call minimal and fast

---

TASK:

1. Import query engine:

from query_engine import execute_query

---

2. Define function:

def route_query(user_query: str):
    """
    Routes user query using LLM → maps to supported intent → executes query
    """

---

STEP 1: HARD GUARDRAIL (before LLM)

If query does NOT contain any of these keywords:
["order", "invoice", "customer", "product", "delivery", "payment"]

→ Immediately return:

{
  "status": "rejected",
  "reason": "Query outside supported dataset domain"
}

---

STEP 2: LLM CLASSIFICATION

Prompt to LLM:

You are a strict query classifier.

Map the user query into EXACTLY one of these formats:

1. orders by customer <ID>
2. products in order <ID>
3. orders without delivery
4. invoices without payment

Rules:
- Return ONLY ONE line
- No explanation
- No extra text
- If query is unrelated → return: REJECT

---

3. Call LLM with user_query

---

STEP 3: VALIDATION

If response:
- == "REJECT" → return rejection
- does not match any valid pattern → reject

---

STEP 4: EXECUTION

Call:

result = execute_query(mapped_query)

---

STEP 5: FINAL RESPONSE FORMAT

Return:

{
  "input_query": user_query,
  "mapped_query": mapped_query,
  "status": "success",
  "data": result
}

---

CONSTRAINTS:

- LLM must NOT access graph
- LLM must NOT generate answers
- LLM is ONLY a mapper
- Keep temperature low (0 or near 0)
- Ensure fast response (<1s if possible)

---

OPTIONAL (GOOD PRACTICE):

Log:
- user_query
- mapped_query
- rejected queries

---

GOAL:

Build a strictly controlled LLM routing layer that ensures:
- zero hallucination
- high precision
- safe usage

Context: Implementing a controlled AI layer to map natural language to structured intents.

### Prompt 6
We already have an LLM Router that maps queries to strict formats.

Now improve it to support more natural language variations.

---

OBJECTIVE:
Enhance llm_router.py to handle flexible user phrasing while staying controlled.

---

TASK:

1. Expand supported variations for each intent:

Intent: orders by customer
- "orders from customer <ID>"
- "what did customer <ID> order"
- "show orders for customer <ID>"

Intent: products in order
- "items in order <ID>"
- "what products are in order <ID>"

Intent: orders without delivery
- "orders not delivered"
- "undelivered orders"
- "pending deliveries"

Intent: invoices without payment
- "unpaid invoices"
- "invoices not paid"
- "pending payments"

---

2. Update LLM prompt:

Add instruction:

"You must normalize flexible natural language into one of the exact supported formats."

---

3. Add fallback rule:

If LLM confidence is unclear → reject

---

4. Add optional keyword mapping BEFORE LLM:

Example:
if "unpaid" in query → map to "invoices without payment"

---

CONSTRAINTS:

- Do NOT use embeddings
- Do NOT use vector DB
- Keep system deterministic
- Maintain guardrails

---

GOAL:

Make system feel intelligent without sacrificing control

Context: Improving conversational flexibility and adding deterministic semantic overrides.

### Outcome
- **Built**: `llm_router.py` with Gemini integration and regex validation.
- **Issue**: Initial model `gemini-1.5-flash` returned 404/not supported errors.
- **Fix**: Updated to stable `gemini-3-flash-preview` alias and added semantic overrides for terms like "unpaid".
- **Result**: Accurate NL-to-Intent mapping without hallucination risks.

---

## Phase 6: UI Development

### Prompt 7
We have a complete backend:

- graph_builder.py
- query_engine.py
- llm_router.py

Now build a SIMPLE but INTERACTIVE UI.

---

OBJECTIVE:
Create a minimal frontend using Streamlit with interactive graph visualization.

---

TASK:

1. Create file: app.py

---

2. UI STRUCTURE:

- Title: "Graph-Based O2C Query System"

- Layout:
  Use st.columns:
    Left → Query Interface
    Right → Graph Visualization

---

3. QUERY INTERFACE (LEFT):

- Text input: user_query
- Button: "Run Query"

On submit:
- Call: route_query(user_query)

Display:
- Mapped Query
- Status (success / rejected)
- Result count
- Result data (use st.json or st.expander)

---

4. GRAPH VISUALIZATION (CRITICAL):

- Use pyvis (Network)
- DO NOT use matplotlib

Steps:

- Load graph using build_graph()
- Convert NetworkX → Pyvis Network
- Save graph as HTML (temp file)

- Render in Streamlit:
  st.components.v1.html(html_content, height=600)

---

INTERACTIVITY REQUIREMENTS:

- Must support:
  - zoom
  - drag
  - node click
  - hover labels

- Each node must display:
  - node id
  - node type

---

5. NODE HIGHLIGHTING (BONUS — HIGH IMPACT):

If query returns nodes:
- Highlight them in graph:
  - Change color (e.g., red)
  - Increase size

All other nodes:
- default color (e.g., blue/gray)

---

6. ERROR HANDLING:

- If query rejected → st.warning
- If error → st.error

---

7. PERFORMANCE:

- Cache graph build using:
  @st.cache_resource

---

CONSTRAINTS:

- Keep UI minimal
- No authentication
- No unnecessary styling
- Focus on clarity + interaction

---

GOAL:

A working system where:

User types query →
LLM maps →
Query executes →
Results show →
Graph updates interactively

Context: Building the Streamlit interactive dashboard with Pyvis network visualization.

### Prompt 8
Improve graph visualization for clarity.

---

TASK:

When a query is executed:

1. Extract result nodes
2. Build SUBGRAPH:
   - Include:
     - result nodes
     - 1-hop neighbors
3. Render ONLY this subgraph (instead of full graph)

---

BONUS:

- Color:
  - result nodes → RED
  - neighbors → ORANGE
  - others → hidden

---

FALLBACK:

If no query → show full graph

---

GOAL:

Make graph readable and meaningful instead of cluttered

Context: Implementing subgraph extraction to reduce visual noise during data investigation.

### Prompt 9
Modify app.py graph rendering logic:

---

If query returns 0 results:

1. Do NOT render full graph
2. Instead show:

st.warning("No results found for this query")

3. Optionally:
- Show empty graph OR
- Show only relevant node type legend

---

If query has results:
- Render subgraph (highlighted)

---

GOAL:
Avoid misleading visualization when no data exists

Context: Handling zero-result states in the UI to maintain clarity.

### Outcome
- **Built**: `app.py` Streamlit dashboard with Pyvis interactive graph.
- **Issue**: Graph was visually cluttered when displaying all 757 nodes at once.
- **Fix**: Implemented subgraph extraction showing only result nodes + 1-hop neighbors.
- **Result**: Clean, investigative UI with red/orange node highlighting.


## Note
This document contains curated prompts and iterations used during development. Non-essential interactions have been removed for clarity.


**Antigravity (AI Assistant) →** This log was generated by **Antigravity**, a powerful agentic AI coding assistant designed by Google DeepMind. The structured evidence above documents the end-to-end engineering workflow, including prompt quality, debugging patterns, and technical iteration cycles.

