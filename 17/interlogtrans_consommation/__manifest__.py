# -*- coding: utf-8 -*-
{
    'name': 'Interlog Transport - Fuel Consumption',
    'version': '17.0.1.0.0',
    'category': 'Transport',
    'summary': 'Fuel consumption management for transport operations',
    'description': """
        Fuel Consumption Management
        ============================
        * Track fuel consumption for vehicles
        * Record fuel purchases and refueling
        * Calculate consumption rates
        * Generate consumption reports
    """,
    'author': 'Interlogtrans',
    'website': 'https://github.com/Reversecube/interlogtrans_consommation',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'fleet',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/fuel_consumption_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
