from odoo import models, fields, api

class InterlogtransConsommation(models.Model):
    _name = 'interlogtrans.consommation'
    _description = 'Consommation de Carburant'
    _inherit = 'fleet.vehicle.cost'
    _order = 'date desc'
    
    vehicle_id = fields.Many2one('fleet.vehicle', 'Véhicule', required=True)
    kilometrage = fields.Float('Kilométrage', digits=(16, 2))
    kilometrage_precedent = fields.Float('Kilométrage Précédent', digits=(16, 2))
    distance_parcourue = fields.Float('Distance', compute='_compute_distance', store=True)
    compteur = fields.Char('Station')
    article = fields.Selection([('gasoil', 'GASOIL'), ('adblue', 'ADBLUE')], 'Carburant', default='gasoil')
    quantite = fields.Float('Quantité', digits=(16, 2))
    prix_par_litre = fields.Float('Prix/L', digits=(16, 2))
    consommation = fields.Float('L/100km', compute='_compute_consommation', store=True)
    
    @api.depends('kilometrage', 'kilometrage_precedent')
    def _compute_distance(self):
        for rec in self:
            rec.distance_parcourue = abs(rec.kilometrage - rec.kilometrage_precedent) if rec.kilometrage and rec.kilometrage_precedent else 0.0
    
    @api.depends('quantite', 'distance_parcourue')
    def _compute_consommation(self):
        for rec in self:
            rec.consommation = (rec.quantite / rec.distance_parcourue) * 100 if rec.distance_parcourue > 0 and rec.quantite > 0 else 0.0
