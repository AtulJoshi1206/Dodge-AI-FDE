SCHEMA = {
    "outbound_delivery_items": {
        "primary_key": "deliveryDocument",
        "foreign_keys": ["plant", "storageLocation"],
        "columns": ["actualDeliveryQuantity", "batch", "deliveryDocument", "deliveryDocumentItem", "deliveryQuantityUnit", "itemBillingBlockReason", "lastChangeDate", "plant", "referenceSdDocument", "referenceSdDocumentItem", "storageLocation"]
    },
    "products": {
        "primary_key": "product",
        "foreign_keys": ["productOldId"],
        "columns": ["product", "productType", "crossPlantStatus", "crossPlantStatusValidityDate", "creationDate", "createdByUser", "lastChangeDate", "lastChangeDateTime", "isMarkedForDeletion", "productOldId", "grossWeight", "weightUnit", "netWeight", "productGroup", "baseUnit", "division", "industrySector"]
    },
    "plants": {
        "primary_key": "plant",
        "foreign_keys": ["addressId"],
        "columns": ["plant", "plantName", "valuationArea", "plantCustomer", "plantSupplier", "factoryCalendar", "defaultPurchasingOrganization", "salesOrganization", "addressId", "plantCategory", "distributionChannel", "division", "language", "isMarkedForArchiving"]
    },
    "sales_order_items": {
        "primary_key": "salesOrderItem",
        "foreign_keys": ["salesOrder", "material", "productionPlant", "storageLocation"],
        "columns": ["salesOrder", "salesOrderItem", "salesOrderItemCategory", "material", "requestedQuantity", "requestedQuantityUnit", "transactionCurrency", "netAmount", "materialGroup", "productionPlant", "storageLocation", "salesDocumentRjcnReason", "itemBillingBlockReason"]
    },
    "product_plants": {
        "primary_key": "product",
        "foreign_keys": ["plant"],
        "columns": ["product", "plant", "countryOfOrigin", "regionOfOrigin", "productionInvtryManagedLoc", "availabilityCheckType", "fiscalYearVariant", "profitCenter", "mrpType"]
    },
    "billing_document_headers": {
        "primary_key": "billingDocument",
        "foreign_keys": ["companyCode", "soldToParty", "accountingDocument"],
        "columns": ["billingDocument", "billingDocumentType", "creationDate", "creationTime", "lastChangeDateTime", "billingDocumentDate", "billingDocumentIsCancelled", "cancelledBillingDocument", "totalNetAmount", "transactionCurrency", "companyCode", "fiscalYear", "accountingDocument", "soldToParty"]
    },
    "outbound_delivery_headers": {
        "primary_key": "deliveryDocument",
        "foreign_keys": [],
        "columns": ["actualGoodsMovementDate", "actualGoodsMovementTime", "creationDate", "creationTime", "deliveryBlockReason", "deliveryDocument", "hdrGeneralIncompletionStatus", "headerBillingBlockReason", "lastChangeDate", "overallGoodsMovementStatus", "overallPickingStatus", "overallProofOfDeliveryStatus", "shippingPoint"]
    },
    "business_partner_addresses": {
        "primary_key": "businessPartner",
        "foreign_keys": ["addressId"],
        "columns": ["businessPartner", "addressId", "validityStartDate", "validityEndDate", "addressUuid", "addressTimeZone", "cityName", "country", "poBox", "poBoxDeviatingCityName", "poBoxDeviatingCountry", "poBoxDeviatingRegion", "poBoxIsWithoutNumber", "poBoxLobbyName", "poBoxPostalCode", "postalCode", "region", "streetName", "taxJurisdiction", "transportZone"]
    },
    "journal_entry_items_accounts_receivable": {
        "primary_key": "accountingDocument",
        "foreign_keys": ["customer", "companyCode", "glAccount", "profitCenter", "costCenter"],
        "columns": ["companyCode", "fiscalYear", "accountingDocument", "glAccount", "referenceDocument", "costCenter", "profitCenter", "transactionCurrency", "amountInTransactionCurrency", "companyCodeCurrency", "amountInCompanyCodeCurrency", "postingDate", "documentDate", "accountingDocumentType", "accountingDocumentItem", "assignmentReference", "lastChangeDateTime", "customer", "financialAccountType", "clearingDate", "clearingAccountingDocument", "clearingDocFiscalYear"]
    },
    "product_storage_locations": {
        "primary_key": "product",
        "foreign_keys": ["plant"],
        "columns": ["product", "plant", "storageLocation", "physicalInventoryBlockInd", "dateOfLastPostedCntUnRstrcdStk"]
    },
    "billing_document_cancellations": {
        "primary_key": "billingDocument",
        "foreign_keys": ["companyCode"],
        "columns": ["billingDocument", "billingDocumentType", "creationDate", "creationTime", "lastChangeDateTime", "billingDocumentDate", "billingDocumentIsCancelled", "cancelledBillingDocument", "totalNetAmount", "transactionCurrency", "companyCode", "fiscalYear", "accountingDocument", "soldToParty"]
    },
    "business_partners": {
        "primary_key": "businessPartner",
        "foreign_keys": ["customer"],
        "columns": ["businessPartner", "customer", "businessPartnerCategory", "businessPartnerFullName", "businessPartnerGrouping", "businessPartnerName", "correspondenceLanguage", "createdByUser", "creationDate", "creationTime", "firstName", "formOfAddress", "industry", "lastChangeDate", "lastName", "organizationBpName1", "organizationBpName2", "businessPartnerIsBlocked", "isMarkedForArchiving"]
    },
    "payments_accounts_receivable": {
        "primary_key": "accountingDocument",
        "foreign_keys": ["customer", "companyCode", "salesDocument", "glAccount", "profitCenter", "costCenter"],
        "columns": ["companyCode", "fiscalYear", "accountingDocument", "accountingDocumentItem", "clearingDate", "clearingAccountingDocument", "clearingDocFiscalYear", "amountInTransactionCurrency", "transactionCurrency", "amountInCompanyCodeCurrency", "companyCodeCurrency", "customer", "invoiceReference", "invoiceReferenceFiscalYear", "salesDocument", "salesDocumentItem", "postingDate", "documentDate", "assignmentReference", "glAccount", "financialAccountType", "profitCenter", "costCenter"]
    },
    "sales_order_schedule_lines": {
        "primary_key": "salesOrder",
        "foreign_keys": [],
        "columns": ["salesOrder", "salesOrderItem", "scheduleLine", "confirmedDeliveryDate", "orderQuantityUnit", "confdOrderQtyByMatlAvailCheck"]
    },
    "billing_document_items": {
        "primary_key": "billingDocumentItem",
        "foreign_keys": ["billingDocument", "material", "referenceSdDocument"],
        "columns": ["billingDocument", "billingDocumentItem", "material", "billingQuantity", "billingQuantityUnit", "netAmount", "transactionCurrency", "referenceSdDocument", "referenceSdDocumentItem"]
    },
    "customer_company_assignments": {
        "primary_key": "customer",
        "foreign_keys": ["companyCode"],
        "columns": ["customer", "companyCode", "accountingClerk", "accountingClerkFaxNumber", "accountingClerkInternetAddress", "accountingClerkPhoneNumber", "alternativePayerAccount", "paymentBlockingReason", "paymentMethodsList", "paymentTerms", "reconciliationAccount", "deletionIndicator", "customerAccountGroup"]
    },
    "product_descriptions": {
        "primary_key": "product",
        "foreign_keys": [],
        "columns": ["product", "language", "productDescription"]
    },
    "sales_order_headers": {
        "primary_key": "salesOrder",
        "foreign_keys": ["soldToParty"],
        "columns": ["salesOrder", "salesOrderType", "salesOrganization", "distributionChannel", "organizationDivision", "salesGroup", "salesOffice", "soldToParty", "creationDate", "createdByUser", "lastChangeDateTime", "totalNetAmount", "overallDeliveryStatus", "overallOrdReltdBillgStatus", "overallSdDocReferenceStatus", "transactionCurrency", "pricingDate", "requestedDeliveryDate", "headerBillingBlockReason", "deliveryBlockReason", "incotermsClassification", "incotermsLocation1", "customerPaymentTerms", "totalCreditCheckStatus"]
    },
    "customer_sales_area_assignments": {
        "primary_key": "customer",
        "foreign_keys": [],
        "columns": ["customer", "salesOrganization", "distributionChannel", "division", "billingIsBlockedForCustomer", "completeDeliveryIsDefined", "creditControlArea", "currency", "customerPaymentTerms", "deliveryPriority", "incotermsClassification", "incotermsLocation1", "salesGroup", "salesOffice", "shippingCondition", "slsUnlmtdOvrdelivIsAllwd", "supplyingPlant", "salesDistrict", "exchangeRateType"]
    },
}
