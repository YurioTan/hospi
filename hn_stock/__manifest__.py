{
    'name': 'Hospi Stock',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom Stock, Product',
    'website': '',
    'description': """
        custom:
        1. only show cost product to user accounting and purchase
    """,
    'data': [
        'views/product_product_view.xml'
    ],
    'depends': ['stock', 'product'],
    'auto_install': False,
    'installable': True,
    'application': False,
}