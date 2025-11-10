# -*- coding: utf-8 -*-
from odoo import models, fields, api

class InterlogtransConsommation(models.Model):
    _name = 'interlogtrans.consommation'
    _description = 'Consommation de Carburant'
    _inherit = 'fleet.vehicle.cost'
    _order = 'date desc'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Véhicule', required=True)
    kilometrage = fields.Float(string='Kilométrage', digits=(16, 2))
    kilometrage_precedent = fields.Float(string='Kilométrage Précédent', digits=(16, 2))
    distance_parcourue = fields.Float(string='Distance', compute='_compute_distance', store=True)
    compteur = fields.Char(string='Station')
    article = fields.Selection([('gasoil', 'GASOIL'), ('adblue', 'ADBLUE')], string='Carburant', default='gasoil')
    quantite = fields.Float(string='Quantité', digits=(16, 2))
    prix_par_litre = fields.Float(string='Prix/L', digits=(16, 2))
    consommation = fields.Float(string='L/100km', compute='_compute_consommation', store=True)

    @api.depends('kilometrage', 'kilometrage_precedent')
    def _compute_distance(self):
        for record in self:
            if record.kilometrage and record.kilometrage_precedent:
                record.distance_parcourue = abs(record.kilometrage - record.kilometrage_precedent)
            else:
                record.distance_parcourue = 0.0

    @api.depends('quantite', 'distance_parcourue')
    def _compute_consommation(self):
        for record in self:
            if record.distance_parcourue > 0 and record.quantite > 0:
                record.consommation = (record.quantite / record.distance_parcourue) * 100.0
            else:
                record.consommation = 0.0
