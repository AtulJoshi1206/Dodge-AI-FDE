import sys
import imp

try:
    schema_mod = imp.load_source('schema', '/Users/atuljoshi/Documents/Projects/Dodge AI/schema.py')
    graph_schema_mod = imp.load_source('graph_schema', '/Users/atuljoshi/Documents/Projects/Dodge AI/graph_schema.py')
except Exception as e:
    print("Error loading modules", e)
    sys.exit(1)

SCHEMA = schema_mod.SCHEMA
GRAPH_SCHEMA = graph_schema_mod.GRAPH_SCHEMA

success = True
for edge in GRAPH_SCHEMA["edges"]:
    # Check join condition
    cond = edge["join_condition"]
    left, right = cond.split(" == ")
    t1, c1 = left.strip().split(".")
    t2, c2 = right.strip().split(".")
    
    if t1 not in SCHEMA or c1 not in SCHEMA[t1]["columns"]:
        print(f"FAILED: {t1}.{c1} not found")
        success = False
    if t2 not in SCHEMA or c2 not in SCHEMA[t2]["columns"]:
        print(f"FAILED: {t2}.{c2} not found")
        success = False

if success:
    print("VALIDATION SUCCESSFUL")
else:
    print("VALIDATION FAILED")
