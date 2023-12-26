{
    'name': 'Hospi Base',
    'version': '14.0.1.0.0',
    'author': 'Amirul',
    'summary': 'Custom Base',
    'website': '',
    'description': """
        custom:
        1. change state code to state name on address format
        3. add document number to accommodate document/form ISO number
    """,
    'data': [
        'data/res_country_data.xml',
        'views/ir_actions_report_views.xml',
    ],
    'depends': ['base'],
    'auto_install': False,
    'installable': True,
    'application': False,
}