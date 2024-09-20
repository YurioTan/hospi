{
    'name': 'Hospi SO',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom SO',
    'website': '',
    'description': """
        custom:
        1. change SO sequence
        2. add CO sequence, menu, field
        3. change report sale
        4. change report invoice
    """,
    'data': [
        'security/hn_sale_security.xml',
        'security/ir.model.access.csv',
        'views/res_patner_view.xml',
        'views/sale_order_view.xml',
        'views/customer_db_view.xml',
        'data/sequences.xml',
        'report/report_sale.xml',
        'report/report_invoice.xml',
    ],
    'depends': ['sale', 'account', 'arkana_base_crm'],
    'auto_install': False,
    'installable': True,
    'application': False,
}