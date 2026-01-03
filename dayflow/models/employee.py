from odoo import models, fields

class DayflowEmployee(models.Model):
    _name = 'dayflow.employee'
    _description = 'Dayflow Employee'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    department = fields.Char(string='Department')
    
    role = fields.Selection([
        ('employee', 'Employee'),
        ('hr', 'HR Manager')
    ], string='Role', default='employee')

    user_id = fields.Many2one('res.users', string='Related User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', string='Currency')

    # Security: groups='base.group_system' ensures only admin/HR can see this field in views.
    # In a real app, define a specific XML group like 'dayflow.group_hr'.
    salary = fields.Float(string='Salary', groups='base.group_system')
