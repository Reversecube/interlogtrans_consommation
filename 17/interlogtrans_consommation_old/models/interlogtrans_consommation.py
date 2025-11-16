# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InterlogtransConsommation(models.Model):
    _name = 'interlogtrans.consommation'
    _description = 'Consommation de Carburant'
    _inherit = 'fleet.vehicle.cost'
    _order = 'date desc'

    # Inherited from fleet.vehicle.cost: date, amount, vehicle_id, description, cost_type, cost_subtype_id
    
    vehicle_id = fields.Many2one('fleet.vehicle', string='Véhicule', required=True)
    
    # Odometer fields
    kilometrage = fields.Float(string='Kilométrage Actuel', digits=(16, 2), help="Kilométrage actuel du véhicule")
    kilometrage_precedent = fields.Float(string='Kilométrage Précédent', digits=(16, 2), help="Kilométrage précédent enregistré")
    distance_parcourue = fields.Float(
        string='Distance Parcourue (km)', 
        compute='_compute_distance', 
        store=True, 
        digits=(16, 2)
    )
    
    # Fuel fields
    compteur = fields.Char(string='Station Service')
    article = fields.Selection([
        ('gasoil', 'GASOIL'),
        ('adblue', 'ADBLUE'),
        ('essence', 'ESSENCE'),
    ], string='Type de Carburant', default='gasoil', required=True)
    
    quantite = fields.Float(string='Quantité (Litres)', digits=(16, 2))
    prix_par_litre = fields.Float(string='Prix par Litre', digits=(16, 4))
    
    # Consumption
    consommation = fields.Float(
        string='Consommation (L/100km)', 
        compute='_compute_consommation', 
        store=True, 
        digits=(16, 2),
        help="Consommation calculée en litres par 100 kilomètres"
    )

    @api.depends('kilometrage', 'kilometrage_precedent')
    def _compute_distance(self):
        """Calcule la distance parcourue entre deux relevés kilométriques"""
        for record in self:
            if record.kilometrage and record.kilometrage_precedent:
                record.distance_parcourue = abs(record.kilometrage - record.kilometrage_precedent)
            else:
                record.distance_parcourue = 0.0

    @api.depends('quantite', 'distance_parcourue')
    def _compute_consommation(self):
        """Calcule la consommation en L/100km"""
        for record in self:
            if record.distance_parcourue > 0 and record.quantite > 0:
                record.consommation = (record.quantite / record.distance_parcourue) * 100.0
            else:
                record.consommation = 0.0

    @api.onchange('quantite', 'prix_par_litre')
    def _onchange_compute_amount(self):
        """Calcule automatiquement le montant total"""
        for record in self:
            if record.quantite and record.prix_par_litre:
                record.amount = record.quantite * record.prix_par_litre



# # -*- coding: utf-8 -*-
# from odoo import models, fields, api

# class InterlogtransConsommation(models.Model):
#     _name = 'interlogtrans.consommation'
#     _description = 'Consommation de Carburant'
#     _inherit = 'fleet.vehicle.cost'
#     _order = 'date desc'

#     vehicle_id = fields.Many2one('fleet.vehicle', string='Véhicule', required=True)
#     kilometrage = fields.Float(string='Kilométrage', digits=(16, 2))
#     kilometrage_precedent = fields.Float(string='Kilométrage Précédent', digits=(16, 2))
#     distance_parcourue = fields.Float(string='Distance', compute='_compute_distance', store=True)
#     compteur = fields.Char(string='Station')
#     article = fields.Selection([('gasoil', 'GASOIL'), ('adblue', 'ADBLUE')], string='Carburant', default='gasoil')
#     quantite = fields.Float(string='Quantité', digits=(16, 2))
#     prix_par_litre = fields.Float(string='Prix/L', digits=(16, 2))
#     consommation = fields.Float(string='L/100km', compute='_compute_consommation', store=True)

#     @api.depends('kilometrage', 'kilometrage_precedent')
#     def _compute_distance(self):
#         for record in self:
#             if record.kilometrage and record.kilometrage_precedent:
#                 record.distance_parcourue = abs(record.kilometrage - record.kilometrage_precedent)
#             else:
#                 record.distance_parcourue = 0.0

#     @api.depends('quantite', 'distance_parcourue')
#     def _compute_consommation(self):
#         for record in self:
#             if record.distance_parcourue > 0 and record.quantite > 0:
#                 record.consommation = (record.quantite / record.distance_parcourue) * 100.0
#             else:
#                 record.consommation = 0.0
