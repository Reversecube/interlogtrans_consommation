{
    'name': 'Interlog Trans - Gestion de Consommation',
    'version': '17.0.1.0.1',
    'category': 'Fleet',
    'summary': 'Module de gestion de consommation de carburant',
    'author': 'Développé par Interlog Trans',
    'website': 'https://github.com/Reversecube',
    'depends': ['fleet','base'],
    'data': [
        # 'security/ir_model_access.xml',
        # 'security/ir.model.access.csv',
        'views/interlogtrans_consommation_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
