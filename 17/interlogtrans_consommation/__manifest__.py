# -*- coding: utf-8 -*-
{
    'name': 'InterlogTrans Consommation',
    'version': '17.0.1.0.0',
    'category': 'Fleet',
    'summary': 'Gestion de Consommation de Carburant',
    'description': """
        Gestion de Consommation de Carburant
        =====================================
        * Suivi de la consommation par véhicule
        * Calcul automatique du montant
        * Calcul automatique de la consommation
        * Intégration avec la gestion de flotte
    """,
    'author': 'Reversecube',
    'website': 'https://github.com/Reversecube',
    'depends': ['base', 'fleet'],
    'data': [
        'security/ir.model.access.csv',
        'data/fuel_station_data.xml',
        'data/fuel_type_data.xml',
        'views/fuel_consumption_views.xml',
        'views/fuel_consumption_menu.xml',
        'report/fuel_consumption_report.xml',
        'report/fuel_consumption_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
