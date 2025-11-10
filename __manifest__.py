{
    'name': 'Interlog Trans - Gestion de Consommation',
    'summary': 'Gestion de la consommation de carburant',
    'description': 'Développé par Reversecube',
    'author': 'Reversecube',
    'version': '17.0.1.0.2',  # Increment version
    'website': 'https://github.com/Reversecube',
    'category': 'Fleet',
    'depends': ['fleet'],
    'data': [
        'security/ir.model.access.csv',
        'views/interlogtrans_consommation_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}