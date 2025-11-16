# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelStation(models.Model):
    _name = 'fuel.station'
    _description = 'Fuel Station'
    _order = 'name'

    name = fields.Char(string='Station Name', required=True)
    code = fields.Char(string='Station Code')
    active = fields.Boolean(default=True)


class FuelType(models.Model):
    _name = 'fuel.type'
    _description = 'Fuel Type'
    _order = 'name'

    name = fields.Char(string='Fuel Type', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)


class FuelConsumptionType(models.Model):
    _name = 'fuel.consumption.type'
    _description = 'Fuel Consumption Type'
    _order = 'name'

    name = fields.Char(string='Type', required=True)
    code = fields.Char(string='Code')
    active = fields.Boolean(default=True)


class FuelConsumption(models.Model):
    _name = 'fuel.consumption'
    _description = 'Fuel Consumption Record'
    _order = 'date desc, id desc'
    _rec_name = 'display_name'

    # Basic Information
    name = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                       default=lambda self: 'New')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    
    # Supplier & Driver
    fournisseur = fields.Char(string='Supplier')
    chauffeur = fields.Char(string='Driver')
    
    # Vehicle Information
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True,
                                 ondelete='restrict', index=True)
    matricule = fields.Char(string='License Plate', related='vehicle_id.license_plate',
                           store=True, readonly=True)
    
    # Fuel Information
    fuel_type_id = fields.Many2one('fuel.type', string='Fuel Type', required=True,
                                    ondelete='restrict')
    produits = fields.Char(string='Products', related='fuel_type_id.name',
                          store=True, readonly=True)
    
    # Distance & Consumption
    kilometrage = fields.Float(string='Odometer Reading', digits=(12, 2),
                               help='Current odometer reading')
    distance = fields.Float(string='Distance (km)', digits=(12, 2),
                           help='Distance traveled since last refuel')
    litres = fields.Float(string='Litres', digits=(12, 3), required=True)
    prix_unitaire = fields.Float(string='Unit Price', digits=(12, 3), required=True)
    
    # Computed Fields
    montant = fields.Float(string='Amount', digits=(12, 4),
                          compute='_compute_montant', store=True, readonly=True)
    consommation = fields.Float(string='Consumption (L/100km)', digits=(12, 2),
                               compute='_compute_consommation', store=True, readonly=True)
    
    # Additional Information
    consumption_type_id = fields.Many2one('fuel.consumption.type', string='Type',
                                         ondelete='restrict')
    type = fields.Char(string='Type Name', related='consumption_type_id.name',
                      store=True, readonly=True)
    mode_paiement = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Chèque'),
        ('card', 'Card'),
        ('transfer', 'Transfer'),
        ('credit', 'Credit')
    ], string='Payment Method', default='cheque')
    
    station_id = fields.Many2one('fuel.station', string='Fuel Station',
                                 ondelete='restrict', required=True)
    station = fields.Char(string='Station Name', related='station_id.name',
                         store=True, readonly=True)
    
    # Notes
    notes = fields.Text(string='Notes')
    
    # Display Name
    display_name = fields.Char(string='Display Name', compute='_compute_display_name',
                              store=True)
    
    # Company
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        """Generate sequence for fuel consumption record"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'fuel.consumption') or 'New'
        return super(FuelConsumption, self).create(vals)

    @api.depends('litres', 'prix_unitaire')
    def _compute_montant(self):
        """Calculate Amount = Litres × Unit Price"""
        for record in self:
            record.montant = record.litres * record.prix_unitaire

    @api.depends('distance', 'litres')
    def _compute_consommation(self):
        """Calculate Consumption = (Litres ÷ Distance) × 100"""
        for record in self:
            if record.distance and record.litres and record.distance > 0:
                # Consumption in L/100km
                record.consommation = (record.litres / record.distance) * 100
            else:
                record.consommation = 0.0

    @api.depends('vehicle_id', 'date', 'fuel_type_id', 'litres')
    def _compute_display_name(self):
        """Compute display name for record"""
        for record in self:
            if record.vehicle_id and record.date:
                record.display_name = f"{record.vehicle_id.license_plate} - {record.date} - {record.litres}L"
            else:
                record.display_name = record.name or 'New'

    @api.constrains('litres', 'prix_unitaire', 'distance')
    def _check_positive_values(self):
        """Ensure positive values for key fields"""
        for record in self:
            if record.litres < 0:
                raise ValidationError("Litres cannot be negative!")
            if record.prix_unitaire < 0:
                raise ValidationError("Unit price cannot be negative!")
            if record.distance < 0:
                raise ValidationError("Distance cannot be negative!")

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        """Auto-fill odometer reading from vehicle"""
        if self.vehicle_id:
            self.kilometrage = self.vehicle_id.odometer

    @api.onchange('kilometrage')
    def _onchange_kilometrage(self):
        """Calculate distance from previous record"""
        if self.vehicle_id and self.kilometrage:
            last_record = self.env['fuel.consumption'].search([
                ('vehicle_id', '=', self.vehicle_id.id),
                ('kilometrage', '!=', False),
                ('id', '!=', self.id or 0)
            ], order='date desc, id desc', limit=1)
            
            if last_record and last_record.kilometrage:
                self.distance = self.kilometrage - last_record.kilometrage
                if self.distance < 0:
                    self.distance = 0


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    fuel_consumption_ids = fields.One2many('fuel.consumption', 'vehicle_id',
                                          string='Fuel Consumption Records')
    fuel_consumption_count = fields.Integer(string='Fuel Records',
                                           compute='_compute_fuel_consumption_count')
    average_consumption = fields.Float(string='Average Consumption (L/100km)',
                                       compute='_compute_average_consumption',
                                       digits=(12, 2))
    total_fuel_cost = fields.Float(string='Total Fuel Cost',
                                   compute='_compute_total_fuel_cost',
                                   digits=(12, 2))

    def _compute_fuel_consumption_count(self):
        """Count fuel consumption records"""
        for vehicle in self:
            vehicle.fuel_consumption_count = len(vehicle.fuel_consumption_ids)

    def _compute_average_consumption(self):
        """Calculate average fuel consumption"""
        for vehicle in self:
            records = vehicle.fuel_consumption_ids.filtered(
                lambda r: r.consommation > 0)
            if records:
                vehicle.average_consumption = sum(
                    records.mapped('consommation')) / len(records)
            else:
                vehicle.average_consumption = 0.0

    def _compute_total_fuel_cost(self):
        """Calculate total fuel cost"""
        for vehicle in self:
            vehicle.total_fuel_cost = sum(
                vehicle.fuel_consumption_ids.mapped('montant'))

    def action_view_fuel_consumption(self):
        """Open fuel consumption records for this vehicle"""
        self.ensure_one()
        return {
            'name': 'Fuel Consumption',
            'type': 'ir.actions.act_window',
            'res_model': 'fuel.consumption',
            'view_mode': 'tree,form,graph,pivot',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id}
        }
