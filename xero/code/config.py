import os

# constants that don't change across clients
TOKEN_URL = 'https://identity.xero.com/connect/token'

endpoint_base = 'https://api.xero.com/api.xro/2.0/'

ENDPOINTS = {
    'accounts': endpoint_base + 'Accounts',
    # 'attachments': endpoint_base + '{Endpoint}/{Guid}/Attachments',
    'bank_transactions': endpoint_base + 'BankTransactions',
    'bank_transfers': endpoint_base + 'BankTransfers',
    'batch_payments': endpoint_base + 'BatchPayments',
    'branding_themes': endpoint_base + 'BrandingThemes',
    'budgets': endpoint_base + 'Budgets',
    'contact_groups': endpoint_base + 'ContactGroups',
    'contacts': endpoint_base + 'Contacts',
    'credit_notes': endpoint_base + 'CreditNotes',
    'currencies': endpoint_base + 'Currencies',
    'employees': endpoint_base + 'Employees',
    # 'history': endpoint_base + '{Endpoint}/{Guid}/history',
    # 'invoice_reminders': endpoint_base + 'InvoiceReminders/Settings',
    'invoices': endpoint_base + 'Invoices',
    'items': endpoint_base + 'Items',
    'journals': endpoint_base + 'Journals',
    'linked_transactions': endpoint_base + 'LinkedTransactions',
    'manual_journals': endpoint_base + 'ManualJournals',
    'organisation': endpoint_base + 'Organisation',
    'overpayments': endpoint_base + 'Overpayments',
    'payment_services': endpoint_base + 'PaymentServices',
    'payments': endpoint_base + 'Payments',
    'prepayments': endpoint_base + 'Prepayments',
    'purchase_orders': endpoint_base + 'PurchaseOrders',
    'quotes': endpoint_base + 'Quotes',
    'repeating_invoices': endpoint_base + 'RepeatingInvoices',
    'reports__balance_sheet': endpoint_base + 'Reports/BalanceSheet',
    'reports__bank_summary': endpoint_base + 'Reports/BankSummary',
    'reports__budget_summary': endpoint_base + 'Reports/BudgetSummary',
    'reports__executive_summary': endpoint_base + 'Reports/ExecutiveSummary',
    # new zealand based onganisations only
    'reports__gst_report': endpoint_base + 'Reports',
    'reports__trial_balance': endpoint_base + 'Reports/TrialBalance',
    'tax_rates': endpoint_base + 'TaxRates',
    'tracking_categories': endpoint_base + 'TrackingCategories',
    'users': endpoint_base + 'Users',
}

def get_env_variable(var_name):
    value = os.environ.get(var_name)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value

def get_client_config():
    client_name = get_env_variable("CLIENT_NAME")
    project_id = get_env_variable("GOOGLE_CLOUD_PROJECT")
    
    return {
        "CLIENT_NAME": client_name,
        "PROJECT_ID": project_id,
        "BUCKET_NAME": f"{project_id}-{client_name}-xero-data",
        "SECRETS_PATH": f"projects/{project_id}/secrets",
    }

CONFIG = {
    **get_client_config(),
    "TOKEN_URL": TOKEN_URL,
    "ENDPOINTS": ENDPOINTS,
}