# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FuelStation(models.Model):
    _name = 'fuel.station'
    _description = 'Station Service'
    _order = 'name'

    name = fields.Char('Nom Station', required=True)
    code = fields.Char('Code')
    active = fields.Boolean('Actif', default=True)


class FuelType(models.Model):
    _name = 'fuel.type'
    _description = 'Type de Carburant'
    _order = 'name'

    name = fields.Char('Type', required=True)
    code = fields.Char('Code')
    active = fields.Boolean('Actif', default=True)


class FuelConsumptionType(models.Model):
    _name = 'fuel.consumption.type'
    _description = 'Type de Consommation'
    _order = 'name'

    name = fields.Char('Type', required=True)
    code = fields.Char('Code')
    active = fields.Boolean('Actif', default=True)


class FuelConsumption(models.Model):
    _name = 'fuel.consumption'
    _description = 'Consommation Carburant'
    _order = 'date desc, id desc'
    _rec_name = 'name'

    name = fields.Char('Référence', required=True, copy=False, readonly=True, default='New')
    date = fields.Date('Date', required=True, default=fields.Date.context_today, index=True)
    
    fournisseur = fields.Char('Fournisseur')
    chauffeur = fields.Char('Chauffeur', index=True)
    
    vehicle_id = fields.Many2one('fleet.vehicle', 'Véhicule', required=True, ondelete='restrict', index=True)
    matricule = fields.Char('Matricule', related='vehicle_id.license_plate', store=True, readonly=True)
    
    fuel_type_id = fields.Many2one('fuel.type', 'Type Carburant', required=True, ondelete='restrict')
    produits = fields.Char('Produits', related='fuel_type_id.name', store=True, readonly=True)
    
    kilometrage = fields.Float('Kilométrage', digits=(12, 2))
    distance = fields.Float('Distance (km)', digits=(12, 2))
    litres = fields.Float('Litres', digits=(12, 3), required=True)
    prix_unitaire = fields.Float('Prix Unitaire', digits=(12, 3), required=True)
    
    montant = fields.Float('Montant Total', digits=(12, 4), compute='_compute_montant', store=True)
    consommation = fields.Float('Consommation (L/100km)', digits=(12, 2), compute='_compute_consommation', store=True)
    
    consumption_type_id = fields.Many2one('fuel.consumption.type', 'Type', ondelete='restrict')
    type = fields.Char('Type', related='consumption_type_id.name', store=True, readonly=True)
    
    mode_paiement = fields.Selection([
        ('cheque', 'Chèque'),
        ('espece', 'Espèce'),
        ('cash', 'Cash'),
        ('card', 'Carte Bancaire'),
        ('transfer', 'Virement'),
        ('credit', 'Crédit')
    ], 'Mode de Paiement', default='cheque', required=True)
    
    station_id = fields.Many2one('fuel.station', 'Station Service', required=True, ondelete='restrict')
    station = fields.Char('Station', related='station_id.name', store=True, readonly=True)
    
    notes = fields.Text('Notes')
    company_id = fields.Many2one('res.company', 'Société', default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fuel.consumption') or 'New'
        return super(FuelConsumption, self).create(vals)

    @api.depends('litres', 'prix_unitaire')
    def _compute_montant(self):
        for rec in self:
            rec.montant = rec.litres * rec.prix_unitaire

    @api.depends('distance', 'litres')
    def _compute_consommation(self):
        for rec in self:
            if rec.distance and rec.litres and rec.distance > 0:
                rec.consommation = (rec.litres / rec.distance) * 100
            else:
                rec.consommation = 0.0

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.kilometrage = self.vehicle_id.odometer

    @api.onchange('kilometrage')
    def _onchange_kilometrage(self):
        if self.vehicle_id and self.kilometrage:
            last = self.env['fuel.consumption'].search([
                ('vehicle_id', '=', self.vehicle_id.id),
                ('kilometrage', '!=', False),
                ('id', '!=', self.id or 0)
            ], order='date desc, id desc', limit=1)
            if last and last.kilometrage:
                self.distance = self.kilometrage - last.kilometrage


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fuel_consumption_ids = fields.One2many('fuel.consumption', 'vehicle_id', 'Consommations')
    fuel_consumption_count = fields.Integer('Nb Consommations', compute='_compute_fuel_count')
    average_consumption = fields.Float('Consommation Moyenne', compute='_compute_avg_consumption', digits=(12, 2))
    total_fuel_cost = fields.Float('Coût Total Carburant', compute='_compute_fuel_cost', digits=(12, 2))

    def _compute_fuel_count(self):
        for rec in self:
            rec.fuel_consumption_count = len(rec.fuel_consumption_ids)

    def _compute_avg_consumption(self):
        for rec in self:
            items = rec.fuel_consumption_ids.filtered(lambda r: r.consommation > 0)
            rec.average_consumption = sum(items.mapped('consommation')) / len(items) if items else 0.0

    def _compute_fuel_cost(self):
        for rec in self:
            rec.total_fuel_cost = sum(rec.fuel_consumption_ids.mapped('montant'))
