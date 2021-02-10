{
    'name': 'Hospi Stock',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom Stock, Product',
    'website': '',
    'description': """
        Custom:\n
        1. Only show cost product to user accounting and purchase
    """,
    'data': [
        'views/product_product_view.xml'
    ],
    'depends': ['base', 'stock', 'product'],
    'auto_install': False,
    'installable': True,
    'application': False,
}