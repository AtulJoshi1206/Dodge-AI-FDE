GRAPH_SCHEMA = {
    "nodes": [
        "Customer",
        "SalesOrder",
        "SalesOrderItem",
        "Product",
        "Delivery",
        "Invoice",
        "Payment",
        "Plant"
    ],
    "edges": [
        {
            "from": "SalesOrder",
            "to": "Customer",
            "relation": "placed_by",
            "source_table": "sales_order_headers",
            "target_table": "business_partners",
            "join_condition": "sales_order_headers.soldToParty == business_partners.customer"
        },
        {
            "from": "SalesOrderItem",
            "to": "SalesOrder",
            "relation": "belongs_to",
            "source_table": "sales_order_items",
            "target_table": "sales_order_headers",
            "join_condition": "sales_order_items.salesOrder == sales_order_headers.salesOrder"
        },
        {
            "from": "SalesOrderItem",
            "to": "Product",
            "relation": "orders_product",
            "source_table": "sales_order_items",
            "target_table": "products",
            "join_condition": "sales_order_items.material == products.product"
        },
        {
            "from": "SalesOrderItem",
            "to": "Plant",
            "relation": "supplied_by",
            "source_table": "sales_order_items",
            "target_table": "plants",
            "join_condition": "sales_order_items.productionPlant == plants.plant"
        },
        {
            "from": "Delivery",
            "to": "SalesOrder",
            "relation": "fulfills",
            "source_table": "outbound_delivery_items",
            "target_table": "sales_order_headers",
            "join_condition": "outbound_delivery_items.referenceSdDocument == sales_order_headers.salesOrder"
        },
        {
            "from": "Invoice",
            "to": "Delivery",
            "relation": "bills_for",
            "source_table": "billing_document_items",
            "target_table": "outbound_delivery_headers",
            "join_condition": "billing_document_items.referenceSdDocument == outbound_delivery_headers.deliveryDocument"
        },
        {
            "from": "Invoice",
            "to": "Customer",
            "relation": "billed_to",
            "source_table": "billing_document_headers",
            "target_table": "business_partners",
            "join_condition": "billing_document_headers.soldToParty == business_partners.customer"
        },
        {
            "from": "Payment",
            "to": "Invoice",
            "relation": "clears",
            "source_table": "payments_accounts_receivable",
            "target_table": "billing_document_headers",
            "join_condition": "payments_accounts_receivable.accountingDocument == billing_document_headers.accountingDocument"
        },
        {
            "from": "Payment",
            "to": "Customer",
            "relation": "paid_by",
            "source_table": "payments_accounts_receivable",
            "target_table": "business_partners",
            "join_condition": "payments_accounts_receivable.customer == business_partners.customer"
        }
    ]
}
