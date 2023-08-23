{
    'name': 'Indonesia Overtime (Lembur)',
    'version': '15.0.1.0.1',
    'summary': 'Form Pengisian Lembur beserta kalkulasi lembur berdasarkan peraturan pemerintah yang di integrasikan dengan modul payroll',
    'author': 'altech.id',
    'description': 'Form Pengisian lembur dengan konfigurasi beserta besaran kalkulasi lembur sesuai dengan peraturan pemerintah.',
    'price' : 520,
    'currency' : 'USD',
    'company': 'altech.id',
    'website': 'https://altech.id',
    'depends': [
        'base','hr','altech_payroll_indonesia'
    ],
    'data': [
        'views/res_config.xml',
        'views/contract_component.xml',
        'views/working_hours.xml',
        'views/overtime_periode.xml',
        'views/overtime_coeficient.xml',
        'views/overtime_calculation.xml',
        'views/overtime_employee.xml',
        'views/menu_items.xml',
        'views/employee.xml',
        'data/overtime.lembur.koefisien.csv',
        'security/ir.model.access.csv'
    ],
    'category': 'Generic Modules/Human Resources',
    'maintainer': 'altech.id',
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
    'support': 'support@altech.co.id',
    'images': ['static/description/banner.jpg'],
}
