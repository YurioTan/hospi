{
    'name': 'Hospi PO',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom PO',
    'website': '',
    'description': """
        custom:
        1. add numbering on product PO (printout)
        2. change default PO sequence
        3. add external reference on product and custom name_get
        4. change table format on PO (printout)
    """,
    'data': [
        'data/sequences.xml',
        'report/purchase_order.xml',
        'views/product_product_view.xml'
    ],
    'depends': ['purchase'],
    'auto_install': False,
    'installable': True,
    'application': False,
}