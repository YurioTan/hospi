{
    'name': 'Hospi Invoice',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom Invoice',
    'website': '',
    'description': """
        Custom:\n
        1. Add amount taxes and show on report invoice,\n
        2. Change report invoice: tax position
    """,
    'data': [
        'views/account_move_view.xml',
        'reports/report_invoice.xml',
    ],
    'depends': ['base', 'account'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
