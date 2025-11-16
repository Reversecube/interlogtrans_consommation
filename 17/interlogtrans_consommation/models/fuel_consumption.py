# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FuelStation(models.Model):
    _name = 'fuel.station'
    _description = 'Fuel Station'

    name = fields.Char(string='Station Name', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)


class FuelType(models.Model):
    _name = 'fuel.type'
    _description = 'Fuel Type'

    name = fields.Char(string='Fuel Type', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)


class FuelConsumptionType(models.Model):
    _name = 'fuel.consumption.type'
    _description = 'Fuel Consumption Type'

    name = fields.Char(string='Type', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)


class FuelConsumption(models.Model):
    _name = 'fuel.consumption'
    _description = 'Fuel Consumption'
    _order = 'date desc'

    name = fields.Char(string='Reference', required=True, default='New')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    
    fournisseur = fields.Char(string='Fournisseur')
    chauffeur = fields.Char(string='Chauffeur')
    
    vehicle_id = fields.Many2one('fleet.vehicle', string='Véhicule', required=True)
    matricule = fields.Char(string='Matricule', related='vehicle_id.license_plate', store=True)
    
    fuel_type_id = fields.Many2one('fuel.type', string='Type Carburant', required=True)
    produits = fields.Char(string='Produits', related='fuel_type_id.name', store=True)
    
    kilometrage = fields.Float(string='Kilométrage (KM)')
    distance = fields.Float(string='Distance (km)')
    litres = fields.Float(string='Litres', required=True)
    prix_unitaire = fields.Float(string='Prix Unitaire', required=True)
    
    montant = fields.Float(string='Montant Total', compute='_compute_montant', store=True)
    consommation = fields.Float(string='Consommation (L/100km)', compute='_compute_consommation', store=True)
    
    consumption_type_id = fields.Many2one('fuel.consumption.type', string='Type')
    type = fields.Char(string='Type Name', related='consumption_type_id.name', store=True)
    
    mode_paiement = fields.Selection([
        ('cheque', 'Chèque'),
        ('espece', 'Espèce'),
        ('cash', 'Cash'),
        ('card', 'Carte'),
        ('transfer', 'Virement'),
    ], string='Mode de Paiement', default='cheque', required=True)
    
    station_id = fields.Many2one('fuel.station', string='Station', required=True)
    station = fields.Char(string='Station Name', related='station_id.name', store=True)
    
    notes = fields.Text(string='Notes')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fuel.consumption') or 'New'
        return super(FuelConsumption, self).create(vals)

    @api.depends('litres', 'prix_unitaire')
    def _compute_montant(self):
        for record in self:
            record.montant = record.litres * record.prix_unitaire

    @api.depends('distance', 'litres')
    def _compute_consommation(self):
        for record in self:
            if record.distance and record.litres and record.distance > 0:
                record.consommation = (record.litres / record.distance) * 100
            else:
                record.consommation = 0.0

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.kilometrage = self.vehicle_id.odometer

    @api.onchange('kilometrage')
    def _onchange_kilometrage(self):
        if self.vehicle_id and self.kilometrage:
            last_record = self.env['fuel.consumption'].search([
                ('vehicle_id', '=', self.vehicle_id.id),
                ('kilometrage', '!=', False),
                ('id', '!=', self.id or 0)
            ], order='date desc', limit=1)
            
            if last_record and last_record.kilometrage:
                self.distance = self.kilometrage - last_record.kilometrage


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fuel_consumption_ids = fields.One2many('fuel.consumption', 'vehicle_id', string='Consommations')
    fuel_consumption_count = fields.Integer(compute='_compute_fuel_count')
    average_consumption = fields.Float(compute='_compute_average_consumption')
    total_fuel_cost = fields.Float(compute='_compute_total_fuel_cost')

    def _compute_fuel_count(self):
        for vehicle in self:
            vehicle.fuel_consumption_count = len(vehicle.fuel_consumption_ids)

    def _compute_average_consumption(self):
        for vehicle in self:
            records = vehicle.fuel_consumption_ids.filtered(lambda r: r.consommation > 0)
            vehicle.average_consumption = sum(records.mapped('consommation')) / len(records) if records else 0.0

    def _compute_total_fuel_cost(self):
        for vehicle in self:
            vehicle.total_fuel_cost = sum(vehicle.fuel_consumption_ids.mapped('montant'))
