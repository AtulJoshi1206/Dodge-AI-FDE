import os
import json
import re

def singular(name):
    # simple rules
    if name.endswith('ies'): return name[:-3] + 'y'
    if name.endswith('s'): return name[:-1]
    return name

data_dir = '/Users/atuljoshi/Documents/Projects/Dodge AI/sap-o2c-data'
schema = {}

for root, dirs, files in os.walk(data_dir):
    for f in files:
        if f.endswith('.jsonl'):
            table_name = os.path.basename(root)
            if table_name not in schema:
                file_path = os.path.join(root, f)
                with open(file_path, 'r') as fp:
                    try:
                        first_line = fp.readline()
                        data = json.loads(first_line)
                        schema[table_name] = {
                            "primary_key": None,
                            "foreign_keys": [],
                            "columns": list(data.keys())
                        }
                    except:
                        pass

# Attempt to infer primary keys
for table, info in schema.items():
    cols = info['columns']
    # If a column exactly matches the singular of the table name (camel case)
    # e.g. 'sales_orders' -> 'salesOrder'
    table_parts = table.split('_')
    camel_singular = table_parts[0] + ''.join(p.capitalize() for p in table_parts[1:])
    if camel_singular.endswith('s') and camel_singular not in cols:
        camel_singular = camel_singular[:-1]
    if camel_singular.endswith('ie') and camel_singular not in cols:
        camel_singular = camel_singular[:-2] + 'y'
        
    candidates = []
    for c in cols:
        # standard SAP ids
        if c.lower() == camel_singular.lower() or c == 'id':
            candidates.append(c)
        elif c in ['salesOrder', 'billingDocument', 'outboundDelivery', 'businessPartner', 'product', 'companyCode', 'plant']:
            if c.lower() in table.lower().replace('_', ''):
                candidates.append(c)

    # for headers/items
    if 'salesOrder' in cols and 'sales_order' in table: candidates.append('salesOrder')
    if 'billingDocument' in cols and 'billing_document' in table: candidates.append('billingDocument')
    if 'outboundDelivery' in cols and 'outbound_delivery' in table: candidates.append('outboundDelivery')

    if candidates:
        info['primary_key'] = candidates[0]
    else:
        info['primary_key'] = cols[0] if cols else None

# Attempt to infer foreign keys based on overlap with other PKs
all_pks = {info['primary_key']: t for t, info in schema.items() if info['primary_key']}
for table, info in schema.items():
    for c in info['columns']:
        if c != info['primary_key']:
            if c in all_pks:
                info['foreign_keys'].append(c)
            elif c.endswith('Id') or c.endswith('_id'): 
                info['foreign_keys'].append(c)

# Format as python file
out_path = '/Users/atuljoshi/Documents/Projects/Dodge AI/schema.py'
with open(out_path, 'w') as f:
    f.write('SCHEMA = {\n')
    for table, info in schema.items():
        f.write(f'    "{table}": {{\n')
        pk_str = f'"{info["primary_key"]}"' if info['primary_key'] else 'None'
        f.write(f'        "primary_key": {pk_str},\n')
        fk_str = '", "'.join(info['foreign_keys'])
        if fk_str: fk_str = f'"{fk_str}"'
        f.write(f'        "foreign_keys": [{fk_str}],\n')
        col_str = '", "'.join(info['columns'])
        f.write(f'        "columns": ["{col_str}"]\n')
        f.write('    },\n')
    f.write('}\n')
