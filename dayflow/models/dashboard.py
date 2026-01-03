from odoo import models, fields, api

class DayflowDashboard(models.Model):
    _name = 'dayflow.dashboard'
    _description = 'Dayflow Dashboard'

    name = fields.Char(string='Name', default='Dashboard')
    employee_count = fields.Integer(string='Total Employees', compute='_compute_counts')
    attendance_count = fields.Integer(string='Present Today', compute='_compute_counts')
    pending_leaves = fields.Integer(string='Pending Leaves', compute='_compute_counts')

    def _compute_counts(self):
        for record in self:
            record.employee_count = self.env['dayflow.employee'].search_count([])
            
            # Count attendance records for today where status is 'present'
            record.attendance_count = self.env['dayflow.attendance'].search_count([
                ('date', '=', fields.Date.today()),
                ('status', '=', 'present')
            ])
            
            # Count leaves where status is 'pending'
            record.pending_leaves = self.env['dayflow.leave'].search_count([
                ('status', '=', 'pending')
            ])

    def unlink(self):
        raise exceptions.UserError("Cannot delete the Dayflow Dashboard!")

    @api.model
    def create(self, vals):
        if self.search_count([]) >= 1:
            raise exceptions.UserError("Only one Dashboard record can exist!")
        return super(DayflowDashboard, self).create(vals)
