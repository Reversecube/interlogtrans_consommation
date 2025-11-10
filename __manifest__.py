{
    'name': 'Interlog Trans - Gestion de Consommation',
    'version': '17.0.1.1.0',  # Change version to trigger upgrade
    'category': 'Fleet',
    'summary': 'Module de gestion de consommation de carburant',
    'author': 'Développé par Interlog Trans',
    'website': 'https://github.com/Reversecube',
    'depends': ['fleet', 'base'],
    'data': [
        'views/interlogtrans_consommation_views.xml',  # Uncommented!
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
