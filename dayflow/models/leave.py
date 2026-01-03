from odoo import models, fields, exceptions

class DayflowLeave(models.Model):
    _name = 'dayflow.leave'
    _description = 'Dayflow Leave Request'

    employee_id = fields.Many2one('dayflow.employee', string='Employee', required=True)
    leave_type = fields.Selection([
        ('paid', 'Paid Leave'),
        ('sick', 'Sick Leave'),
        ('unpaid', 'Unpaid Leave')
    ], string='Leave Type', required=True)
    
    from_date = fields.Date(string='From Date', required=True)
    to_date = fields.Date(string='To Date', required=True)
    number_of_days = fields.Integer(string='Duration (Days)', compute='_compute_days', store=True)
    
    status = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='pending', copy=False)

    @api.constrains('from_date', 'to_date', 'employee_id')
    def _check_overlap(self):
        for record in self:
            if record.from_date > record.to_date:
                raise exceptions.ValidationError("From Date cannot be after To Date!")
            
            domain = [
                ('id', '!=', record.id),
                ('employee_id', '=', record.employee_id.id),
                ('status', 'in', ['pending', 'approved']),
                ('from_date', '<=', record.to_date),
                ('to_date', '>=', record.from_date)
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError("You already have a leave request for this period!")

    @api.depends('from_date', 'to_date')
    def _compute_days(self):
        for record in self:
            if record.from_date and record.to_date:
                delta = record.to_date - record.from_date
                record.number_of_days = delta.days + 1
            else:
                record.number_of_days = 0

    def action_approve(self):
        for record in self:
            if record.status != 'pending':
                raise exceptions.UserError("Only pending requests can be approved.")
            record.status = 'approved'

    def action_reject(self):
        for record in self:
            if record.status != 'pending':
                raise exceptions.UserError("Only pending requests can be rejected.")
            record.status = 'rejected'
