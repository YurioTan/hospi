{
    'name': 'Hospi SO',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom SO',
    'website': '',
    'description': """
    """,
    'data': [
        'views/sale_order_view.xml',
        'data/sequences.xml',
        'report/sale_order.xml',
    ],
    'depends': ['sale', 'account'],
    'auto_install': False,
    'installable': True,
    'application': False,
}