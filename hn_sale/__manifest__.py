{
    'name': 'Hospi SO',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom SO',
    'website': '',
    'description': """
        Custom:\n
        1. Change SO sequence\n
        2. Add CO sequence, menu, field\n
        3. Change report sale
    """,
    'data': [
        'views/sale_order_view.xml',
        'data/sequences.xml',
        'report/report_sale.xml',
    ],
    'depends': ['base', 'sale', 'account'],
    'auto_install': False,
    'installable': True,
    'application': False,
}