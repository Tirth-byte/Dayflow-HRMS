from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Custom field to show status easily on dashboards
    dayflow_status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'On Leave')
    ], string="Dayflow Status", compute='_compute_dayflow_status')

    @api.depends('attendance_state')
    def _compute_dayflow_status(self):
        for employee in self:
            if employee.attendance_state == 'checked_in':
                employee.dayflow_status = 'present'
            else:
                employee.dayflow_status = 'absent'
