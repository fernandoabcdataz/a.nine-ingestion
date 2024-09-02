import os

# constants that don't change across clients
TOKEN_URL = 'https://identity.xero.com/connect/token'

ENDPOINTS = {
    'accounts': 'https://api.xero.com/api.xro/2.0/Accounts',
    # 'attachments': 'https://api.xero.com/api.xro/2.0/{Endpoint}/{Guid}/Attachments',
    'bank_transactions': 'https://api.xero.com/api.xro/2.0/BankTransactions',
    'bank_transfers': 'https://api.xero.com/api.xro/2.0/BankTransfers',
    'batch_payments': 'https://api.xero.com/api.xro/2.0/BatchPayments',
    'branding_themes': 'https://api.xero.com/api.xro/2.0/BrandingThemes',
    'budgets': 'https://api.xero.com/api.xro/2.0/Budgets',
    'contact_groups': 'https://api.xero.com/api.xro/2.0/ContactGroups',
    'contacts': 'https://api.xero.com/api.xro/2.0/Contacts',
    'credit_notes': 'https://api.xero.com/api.xro/2.0/CreditNotes',
    'currencies': 'https://api.xero.com/api.xro/2.0/Currencies',
    'employees': 'https://api.xero.com/api.xro/2.0/Employees',
    # 'history': 'https://api.xero.com/api.xro/2.0/{Endpoint}/{Guid}/history',
    # 'invoice_reminders': 'https://api.xero.com/api.xro/2.0/InvoiceReminders/Settings',
    'invoices': 'https://api.xero.com/api.xro/2.0/Invoices',
    'items': 'https://api.xero.com/api.xro/2.0/Items',
    'journals': 'https://api.xero.com/api.xro/2.0/Journals',
    'linked_transactions': 'https://api.xero.com/api.xro/2.0/LinkedTransactions',
    'manual_journals': 'https://api.xero.com/api.xro/2.0/ManualJournals',
    'organisation': 'https://api.xero.com/api.xro/2.0/Organisation',
    'overpayments': 'https://api.xero.com/api.xro/2.0/Overpayments',
    'payment_services': 'https://api.xero.com/api.xro/2.0/PaymentServices',
    'payments': 'https://api.xero.com/api.xro/2.0/Payments',
    'prepayments': 'https://api.xero.com/api.xro/2.0/Prepayments',
    'purchase_orders': 'https://api.xero.com/api.xro/2.0/PurchaseOrders',
    'quotes': 'https://api.xero.com/api.xro/2.0/Quotes',
    'repeating_invoices': 'https://api.xero.com/api.xro/2.0/RepeatingInvoices',
    'reports__balance_sheet': 'https://api.xero.com/api.xro/2.0/Reports/BalanceSheet',
    'reports__bank_summary': 'https://api.xero.com/api.xro/2.0/Reports/BankSummary',
    'reports__budget_summary': 'https://api.xero.com/api.xro/2.0/Reports/BudgetSummary',
    'reports__executive_summary': 'https://api.xero.com/api.xro/2.0/Reports/ExecutiveSummary',
    # new zealand based onganisations only
    'reports__gst_report': 'https://api.xero.com/api.xro/2.0/Reports',
    'reports__trial_balance': 'https://api.xero.com/api.xro/2.0/Reports/TrialBalance',
    'tax_rates': 'https://api.xero.com/api.xro/2.0/TaxRates',
    'tracking_categories': 'https://api.xero.com/api.xro/2.0/TrackingCategories',
    'users': 'https://api.xero.com/api.xro/2.0/Users',
}

DEFAULT_CLIENT_NAME = os.getenv("CLIENT_NAME", "default_client")
DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "default_project")

def get_client_config():
    client_name = DEFAULT_CLIENT_NAME
    project_id = DEFAULT_PROJECT_ID

    bucket_name = f"{project_id}-{client_name}-xero-data"
    secrets_path = f"projects/{project_id}/secrets"

    return {
        "CLIENT_NAME": client_name,
        "PROJECT_ID": project_id,
        "BUCKET_NAME": bucket_name,
        "SECRETS_PATH": secrets_path,
    }

CLIENT_CONFIG = get_client_config()

CONFIG = {
    **CLIENT_CONFIG,
    "TOKEN_URL": TOKEN_URL,
    "ENDPOINTS": ENDPOINTS,
}