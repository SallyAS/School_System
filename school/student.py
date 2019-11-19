from odoo import models, fields, api ,_
from odoo.exceptions import ValidationError

class scientific_subjects_information(models.Model):

    _name = "scientific.subjects.information"
    _order = 'id desc'
    _description = "A register of All Scientific Subjects"
    _res_name = "code"

    code = fields.Char("Subjects Code" ,required=True)
    name = fields.Char("Subjects Name" , required=True)

    _sql_constraints = [
        (
         'dorf_code_unique',
         'UNIQUE(code)',
         'Scientific Subjects Code must be Unique',
         )
    ]

class degrees_information(models.Model):
    _name = "degrees.information"
    _order = 'id desc'
    _description = "A register of All Degrees Information"

    name = fields.Char("Degree Name", required=True)
    range_from = fields.Float("From", required=True)
    range_to = fields.Float("To", required=True)

    _sql_constraints = [
        (
         'dorf_name_unique',
         'UNIQUE(name)',
         'Degree Name must be Unique',
         )
    ]

    @api.constrains('range_from' , 'range_to')
    def _check_something(self):
        for record in self:
            if record.range_from < 0 :
                raise ValidationError("Your From record must be More than 0 : %s" %  record.range_from)
            if record.range_to >100:
                raise ValidationError("Your To record must be Less than 100 : %s" %  record.range_to)

class lecturer_information(models.Model):
    _name = "lecturer.information"
    _order = 'id desc'
    _description = "A register of All Lecturers"

    name = fields.Char("Lecturer Name" , required=True)
    subjects = fields.Many2many('scientific.subjects.information',string='Lecturer Subjects')
    image = fields.Char("Image")
    national_id = fields.Char("National ID")
    phone = fields.Char("Phone Number")
    #educational_qualification = fields.Char("Educational Qualification")
    educational_qualification = fields.Selection(
                                     [('GC', 'Graduation Certificate'),
                                      ('GD', 'Graduation Diploma'),
                                      ('BD', 'Bachelor Degree'),
                                      ('BA', 'BA (Hons)'),
                                      ('MD', 'Master Degree'),
                                      ('PH.D', 'Ph.D'),
                                      ('AD', 'Associate Degree'),
                                      ], default='GC')

class Student_information(models.Model):

    _name = "student.information"
    _order = 'id desc'
    _description = "A register of All Students"

    code = fields.Char("Code" , required=True)
    name = fields.Char("Student Name" , required=True)
    year = fields.Char("Year" , required=True)
    image = fields.Char("Image")
    date_of_birth = fields.Date(string='Date of Birth')
    national_id = fields.Char("National ID")
    students_subjects = fields.One2many('student.subject','student_ids',string='Student Subjects')
    students_degrees = fields.One2many('student.degree','student_ids',string='Student Degrees')
    students_payment = fields.One2many('account.invoice', 'student_ids', string='Student Payment')

    @api.multi
    def action_view_payment(self):
        view_id = self.env.ref('account.invoice_tree').id
        invoice_ids = self.env['account.invoice'].search([('student_ids', '=', self.id)]).ids
        return {
            'domain': [('id', 'in', invoice_ids)],
            'name': _('Invoices'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'account.invoice',
            'view_id': view_id,
            'type': 'ir.actions.act_window'
        }

class student_subject(models.Model):
    _name = "student.subject"
    _order = 'id desc'
    student_ids = fields.Many2one('student.information')
    subject_ids = fields.Many2one('scientific.subjects.information',"Subject Name")
    code = fields.Char("Code" ,related='subject_ids.code',store=True)

class student_degree(models.Model):
    _name = "student.degree"
    _order = 'id desc'
    student_ids = fields.Many2one('student.information')
    degree_ids = fields.Many2one('degrees.information', "Degree")
    name = fields.Char("Degree Name", related='degree_ids.name', store=True)

class employee_information(models.Model):
    _name = "employee.information"
    _order = 'id desc'
    _description = "A register of All Employees"

    name = fields.Char("Employee Name", required=True)
    image = fields.Char("Image")
    national_id = fields.Char("National ID")
    phone = fields.Char("Phone Number")
    employee_type = fields.Selection(
        [('MG', 'مدير'),
         ('TR', 'مدرس'),
         ('EM', 'عامل'),
        ], default='MG')

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    student_payment = fields.Char("Student Payment")
    student_ids = fields.Many2one('student.information')

