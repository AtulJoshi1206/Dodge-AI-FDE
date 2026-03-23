# Graph-Based O2C Query System

## 1. Overview
The **Graph-Based O2C Query System** is a specialized investigative tool designed to transform fragmented SAP Order-to-Cash (O2C) datasets into a unified, navigable graph model. By shifting from a relational-first to a relationship-first architecture, the system enables rapid tracing of complex business flows and immediate detection of operational gaps—such as unfulfilled orders or unpaid invoices—that are traditionally difficult to identify in standard ERP reporting.

---

## 2. Key Idea
The core philosophy of this project is **Deterministic AI Integration**. Instead of allowing an LLM to generate code or "guess" at data values (which risks high hallucination in sensitive ERP contexts), we use a structured graph as the source of truth. The LLM acts solely as a **Strict Router**, translating natural language into 100% predictable graph traversal logic.

---

## 3. System Flow
1. **Data Ingestion**: SAP JSONL files (Orders, Deliveries, Invoices, Payments) are loaded.
2. **Graph Construction**: Entities are mapped to nodes; business rules define directional edges.
3. **Natural Language Routing**: User queries are analyzed by Gemini to identify intent and ID.
4. **Deterministic Traversal**: the Query Engine executes hardcoded graph pathfinding.
5. **Interactive Visualization**: Resulting subgraphs are rendered for human investigation.

---

## 4. Architecture

### **Graph Builder (`graph_builder.py`)**
- Built using **NetworkX** and **Pandas** for high-performance relationship mapping.
- Implements a unified ID system (e.g., `SalesOrder_ID`) to prevent collisions across tables.
- Automatically handles 19+ SAP tables, consolidating Headers, Items, and Partners into a cohesive DiGraph.

### **Query Engine (`query_engine.py`)**
- A zero-AI execution layer that performs direct graph traversals.
- Uses semantic edge attributes (e.g., `placed_by`, `fulfills`, `clears`) to navigate the document flow.
- Supports both forward-flow (Order → Payment) and reverse-lookup (Payment → Order) logic.

### **LLM Router (`llm_router.py`)**
- Leverages the **Gemini API** as a stateless intent classifier with a zero-temperature configuration.
- Normalizes conversational phrasing (e.g., "what did X buy?") into strict internal query formats.
- Includes hardcoded semantic overrides for high-frequency terms to reduce API dependency and latency.

### **UI Layer (`app.py`)**
- Developed with **Streamlit** and **Pyvis** for a lightweight, interactive dashboard.
- Features dynamic **Subgraph Rendering**, which automatically filters the view to show only relevant results and their immediate neighbors.
- Implements color-coded visual cues: **Red** for result nodes and **Orange** for contextual neighbors.

---

## 5. Features
- **Conversational ERP Access**: Query complex data without knowing table names or SQL syntax.
- **Broken Flow Detection**: Instant identification of unlinked documents (e.g., deliveries without invoices).
- **Interactive Graph Explorer**: Zoomable, draggable interface with hover-state metadata.
- **Dynamic Subgraphs**: Prevents visual clutter by isolating queried document chains.
- **Explainable Results**: Every answer is backed by a visible path in the O2C network.

---

## 6. Guardrails & Safety
- **Keyword Filtering**: A hard-coded guardrail rejects off-domain queries before calling the LLM.
- **No-Generation Policy**: The system never "creates" data or code; it only executes predefined graph traversals.
- **Input Validation**: Strict Regex verification ensures routed queries adhere to supported patterns.
- **Environment Isolation**: API keys and environment variables are managed via `.env` files.
- **Deterministic Reliability**: The graph structure acts as an absolute constraint against AI drift.

---

## 7. Example Queries
- `"orders by customer 310000108"`
- `"what did customer 310000108 order?"`
- `"which products are in order 740506?"`
- `"show me all undelivered orders"`
- `"find all unpaid invoices"`

<img width="2940" height="4372" alt="image" src="https://github.com/user-attachments/assets/5104b1d8-5d36-469d-8681-a473e6d541e0" />

---

## 8. Real-World Impact
In a production SAP environment, O2C data is often spread across hundreds of tables (VBAK, VBAP, LIKP, VBRK, etc.). This system reduces the time to investigate a "lost" order or a payment mismatch from minutes of manual SQL/SE16 lookups to seconds of natural language interaction. It provides **immediate visibility** into the state of the business lifecycle, enabling faster resolution of revenue-leakage issues.

---

## 9. Setup Instructions
1. **Clone & Install**:
   ```bash
   pip install streamlit networkx pandas pyvis google-generativeai python-dotenv
   ```
2. **Configure API**:
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY='your_gemini_api_key_here'
   ```
3. **Run Application**:
   ```bash
   streamlit run app.py
   ```

---

## 10. Design Decisions
- **NetworkX over Neo4j**: Chosen for rapid prototyping and in-memory performance on medium-sized datasets. It allows for complex logic without the overhead of external database management.
- **LLM as Router, Not Generator**: Decisions were made to eliminate ERP hallucination. By using the LLM only for intent-mapping, we maintain 100% data integrity.
- **Subgraph Rendering**: Full graphs of 700+ nodes are unusable. Filtering to result subgraphs (1-hop neighbors) ensures the UI is an actual investigative tool, not just a "pretty" visual.
- **Heuristic PK/FK Inference**: Automated the schema build by inferring SAP-specific naming conventions, significantly reducing manual mapping time.

---

## 11. Future Improvements
- **Neo4j/GraphDB Integration**: For scaling to millions of transactions.
- **Temporal Graph Analysis**: Adding timestamps to edges to identify O2C bottlenecks and lead-time anomalies.
- **Anomaly Detection Algorithms**: Using graph-centrality or community detection to find unusual purchasing or payment behaviors.
- **Multi-Hop Conversational memory**: Allowing the LLM to handle follow-up questions within a single session.

---

## 12. Conclusion
The **Graph-Based O2C Query System** demonstrates a modern approach to enterprise data interaction. By combining the flexibility of LLMs with the absolute reliability of deterministic graph logic, we create a system that is both intuitive for users and trusted by engineers. It prioritizes **accuracy over guesswork** and provides a clear blueprint for how AI can be safely integrated into the heart of business operations.
