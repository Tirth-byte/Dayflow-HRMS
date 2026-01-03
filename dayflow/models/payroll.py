# dayflow/models/payroll.py
from odoo import models, fields, api

class DayflowPayslip(models.Model):
    _name = 'dayflow.payslip'
    _description = 'Dayflow Payslip'

    employee_id = fields.Many2one('dayflow.employee', string='Employee', required=True)
    currency_id = fields.Many2one('res.currency', related='employee_id.currency_id', string='Currency')
    date_start = fields.Date(string='Date From', required=True)
    date_end = fields.Date(string='Date To', required=True)
    
    gross_wage = fields.Float(string='Gross Wage', compute='_compute_from_contract', store=True, readonly=False, groups="dayflow.group_dayflow_manager")
    bonus = fields.Float(string='Bonus', default=0.0, groups="dayflow.group_dayflow_manager")
    deductions = fields.Float(string='Deductions', default=0.0, groups="dayflow.group_dayflow_manager")
    tax = fields.Float(string='Tax', default=0.0, groups="dayflow.group_dayflow_manager")
    
    net_wage = fields.Float(string='Net Wage', compute='_compute_net', store=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Paid'),
    ], string='Status', default='draft')

    @api.constrains('gross_wage', 'deductions', 'bonus', 'tax')
    def _check_positive(self):
        for record in self:
            if any(f < 0 for f in [record.gross_wage, record.deductions, record.bonus, record.tax]):
                raise exceptions.ValidationError("Payroll values must be positive!")

    @api.depends('employee_id')
    def _compute_from_contract(self):
        for record in self:
            if record.employee_id:
                record.gross_wage = record.employee_id.salary
            else:
                record.gross_wage = 0.0

    @api.depends('gross_wage', 'bonus', 'deductions', 'tax')
    def _compute_net(self):
        for record in self:
            record.net_wage = record.gross_wage + record.bonus - record.deductions - record.tax

    def action_confirm(self):
        self.state = 'done'
