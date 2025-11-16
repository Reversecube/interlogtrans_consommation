# Interlog Trans - Module de Gestion de Consommation

## Description

Module Odoo pour la gestion de la consommation de carburant pour **Interlog Trans**, entreprise de transport routier basée à Tanger, Maroc.

Website: [https://www.interlogtrans.com](https://www.interlogtrans.com)

## Fonctionnalités

✅ **Suivi de consommation** - Calculez automatiquement la consommation (L/100km)  
✅ **Intégration Fleet** - Récupération automatique des données kilométriques  
✅ **Groupement véhicule** - Vue groupée par véhicule avec mise en évidence  
✅ **Workflow de validation** - États: Brouillon → Confirmé → Terminé  
✅ **Design personnalisé** - Couleurs Interlog Trans (Navy Blue & Red)  
✅ **Multi-vues** - Tree, Form, Kanban, Graph, Pivot  
✅ **Rapports** - Analyses de consommation par véhicule/période  

## Installation

1. Copiez le dossier `interlogtrans_consommation` dans votre répertoire addons Odoo
2. Redémarrez le service Odoo
3. Allez dans Apps → Mettre à jour la liste des applications
4. Recherchez "Interlog Trans"
5. Cliquez sur "Installer"

## Configuration

Aucune configuration spéciale requise. Le module s'intègre automatiquement avec:
- Module `fleet` (Flotte de véhicules)
- Model `fleet.vehicle.odometer` (Relevés kilométriques)

## Utilisation

### Créer un relevé de consommation

1. Menu: **Interlog Trans → Consommation**
2. Cliquez sur "Créer"
3. Sélectionnez le véhicule (les données kilométriques se remplissent automatiquement)
4. Renseignez:
   - Station-service
   - Type de carburant (GASOIL, ADBLUE, ESSENCE)
   - Quantité en litres
   - Prix par litre
5. La consommation est calculée automatiquement

### Grouper par véhicule

Par défaut, la vue tree est groupée par véhicule avec:
- **Rouge** pour les enregistrements avec consommation
- **Vert** pour les enregistrements terminés
- **Bleu** pour les enregistrements confirmés

## Structure des fichiers

interlogtrans_consommation/
├── init.py
├── manifest.py
├── models/
│ ├── init.py
│ └── interlogtrans_consommation.py
├── views/
│ └── interlogtrans_consommation_views.xml
├── security/
│ └── ir.model.access.csv
├── data/
│ └── sequence_data.xml
└── README.md

## Champs principaux

| Champ | Type | Description |
|-------|------|-------------|
| `name` | Char | Référence auto-générée (ITC/2025/00001) |
| `vehicle_id` | Many2one | Véhicule concerné |
| `driver_id` | Many2one | Conducteur |
| `kilometrage` | Float | Kilométrage actuel |
| `quantite` | Float | Quantité de carburant (L) |
| `consommation` | Float | Consommation calculée (L/100km) |
| `prix_total` | Monetary | Prix total payé |

## Support

Pour toute question ou support:
- Email: contact@interlogtrans.com
- Website: https://www.interlogtrans.com

## License

LGPL-3

## Auteur

**Interlog Trans** - Expert en Transport Routier National et International  
Tanger, Maroc
