# -*- coding: utf-8 -*-
{
    'name': 'Interlog Trans - Gestion de Consommation',
    'version': '1.0.0',
    'category': 'Fleet',
    'summary': 'Gestion de la consommation de carburant',
    'author': 'Interlog Trans',
    'website': 'https://www.interlogtrans.com',
    'depends': ['base', 'fleet', 'mail'],
    'data': [
        #'security/ir.model.access.csv',  # ← CSV instead of XML
        #'security/security.xml',  # ← COMMENTED FOR INITIAL INSTALL
        #'data/sequence_data.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
