from odoo import models, fields, api, exceptions
from datetime import datetime

class DayflowAttendance(models.Model):
    _name = 'dayflow.attendance'
    _description = 'Dayflow Attendance'
    _order = 'date desc, id desc' # Show latest first
    _sql_constraints = [
        ('employee_date_unique', 'unique(employee_id, date)', 'Employees can only have one attendance record per day!')
    ]

    employee_id = fields.Many2one('dayflow.employee', string='Employee', required=True)
    date = fields.Date(string='Date', default=fields.Date.context_today, required=True)
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    
    status = fields.Selection([
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day')
    ], string='Status', compute='_compute_status', store=True)

    @api.depends('check_in', 'check_out')
    def _compute_status(self):
        for record in self:
            if record.check_in and record.check_out:
                record.status = 'present'
            elif record.check_in:
                record.status = 'present' # Currently present
            else:
                record.status = 'absent'

    @api.constrains('check_in', 'check_out')
    def _check_times(self):
        for record in self:
            if record.check_in and record.check_out and record.check_in > record.check_out:
                raise exceptions.ValidationError("Check Out cannot be before Check In!")

    def action_check_in(self):
        self.ensure_one()
        if self.check_in:
            raise exceptions.UserError("Already checked in!")
        self.check_in = fields.Datetime.now()

    def action_check_out(self):
        self.ensure_one()
        if not self.check_in:
            raise exceptions.UserError("Cannot check out without checking in!")
        self.check_out = fields.Datetime.now()
