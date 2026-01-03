{
    'name': 'Dayflow HRMS Core',
    'version': '1.0',
    'summary': 'Local-first HRMS Core Module for Dayflow',
    'description': """
        Dayflow HRMS: Core customizations.
        - Custom Menu Structure
        - HR Enhancements
        - Attendance Kiosk customizations
    """,
    'category': 'Human Resources',
    'author': 'Dayflow Team',
    'depends': ['base', 'hr', 'hr_attendance', 'hr_holidays'],
    'data': [
        'security/dayflow_security.xml',
        'security/ir.model.access.csv',
        'views/dayflow_menus.xml',
    ],
    'installable': True,
    'application': True,
    'icon': '/dayflow_core/static/description/icon.png',
}
