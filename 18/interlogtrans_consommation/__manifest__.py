# -*- coding: utf-8 -*-
{
    'name': 'InterlogTrans - Fuel Consumption Management',
    'version': '18.0.1.0.0',
    'category': 'Fleet',
    'summary': 'Complete Fuel Consumption Tracking with Auto-Calculations',
    'description': """
        Advanced Fuel Consumption Management Module
        ============================================
        * Track fuel consumption by vehicle, driver, and supplier
        * Automatic calculation of Amount (Litres × Unit Price)
        * Automatic consumption calculation (Distance ÷ Litres)
        * Integration with Fleet Management
        * Support for multiple fuel types (Gasoil, AdBlue)
        * Multiple payment methods tracking
        * Fuel station management
        * Comprehensive reporting
    """,
    'author': 'Reversecube',
    'website': 'https://github.com/Reversecube',
    'depends': ['base', 'fleet', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/fuel_station_data.xml',
        'data/fuel_type_data.xml',
        'views/fuel_consumption_views.xml',
        'views/fuel_consumption_menu.xml',
        'report/fuel_consumption_report.xml',
        'report/fuel_consumption_report_template.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
