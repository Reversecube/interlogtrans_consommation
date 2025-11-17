# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelConsumption(models.Model):
    _name = 'fuel.consumption'
    _description = 'Fuel Consumption Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New'
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        required=True,
        tracking=True
    )
    
    driver_id = fields.Many2one(
        'res.partner',
        string='Driver',
        tracking=True
    )
    
    odometer = fields.Float(
        string='Odometer (km)',
        required=True,
        help='Current odometer reading',
        tracking=True
    )
    
    fuel_type = fields.Selection([
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('lpg', 'LPG'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ], string='Fuel Type', required=True, default='diesel')
    
    quantity = fields.Float(
        string='Quantity (L)',
        required=True,
        help='Fuel quantity in liters',
        tracking=True
    )
    
    price_per_unit = fields.Float(
        string='Price per Liter',
        required=True,
        tracking=True
    )
    
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        tracking=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    station = fields.Char(
        string='Gas Station',
        help='Name or location of gas station'
    )
    
    invoice_number = fields.Char(
        string='Invoice Number'
    )
    
    distance_traveled = fields.Float(
        string='Distance Since Last Fill (km)',
        compute='_compute_distance_traveled',
        store=True
    )
    
    consumption_rate = fields.Float(
        string='Consumption (L/100km)',
        compute='_compute_consumption_rate',
        store=True,
        help='Fuel consumption per 100 kilometers'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    notes = fields.Text(
        string='Notes'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    @api.depends('quantity', 'price_per_unit')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.quantity * record.price_per_unit

    @api.depends('vehicle_id', 'odometer')
    def _compute_distance_traveled(self):
        for record in self:
            if record.vehicle_id and record.odometer:
                previous = self.search([
                    ('vehicle_id', '=', record.vehicle_id.id),
                    ('odometer', '<', record.odometer),
                    ('state', '=', 'confirmed'),
                    ('id', '!=', record.id)
                ], order='odometer desc', limit=1)
                
                if previous:
                    record.distance_traveled = record.odometer - previous.odometer
                else:
                    record.distance_traveled = 0.0
            else:
                record.distance_traveled = 0.0

    @api.depends('quantity', 'distance_traveled')
    def _compute_consumption_rate(self):
        for record in self:
            if record.distance_traveled > 0 and record.quantity > 0:
                record.consumption_rate = (record.quantity / record.distance_traveled) * 100
            else:
                record.consumption_rate = 0.0

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('fuel.consumption') or 'New'
        return super(FuelConsumption, self).create(vals)

    @api.constrains('quantity', 'price_per_unit', 'odometer')
    def _check_positive_values(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("Quantity must be positive!")
            if record.price_per_unit < 0:
                raise ValidationError("Price per unit cannot be negative!")
            if record.odometer < 0:
                raise ValidationError("Odometer reading cannot be negative!")

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
