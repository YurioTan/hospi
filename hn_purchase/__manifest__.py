{
    'name': 'Hospi PO',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom PO',
    'website': '',
    'description': """
        Custom:\n
        1. Add numbering on product PO (printout)\n
        2. Change default PO sequence\n
        3. Add external reference on product and custom name_get\n
        4. Change table format on PO (printout)
    """,
    'data': [
        'data/sequences.xml',
        'report/purchase_order.xml',
        'views/product_product_view.xml'
    ],
    'depends': ['base', 'purchase'],
    'auto_install': False,
    'installable': True,
    'application': False,
}