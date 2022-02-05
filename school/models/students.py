from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class Students(models.Model):
    _name = "school.students"
    _description = "Students"

    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # tracking=True is track whenever you change the data of record
    # it will make a note that show what has been changed in chatbox in bottom of the edit form view
    # but you will need to make a chatbox so this tracking note can be show

    # copy = False is to ignore from copy() function
    # when you add this copy = False, the attribute won't be copy when you click dupplicate

    # this field is for sequence id
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'), tracking=True)
    name = fields.Char(string='Name', tracking=True)
    middle_name = fields.Char(string='Middle Name', required=True, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, tracking=True)
    photo = fields.Binary(string='Photo', tracking=True)
    student_age = fields.Integer(string='Age', tracking=True, copy=False)
    student_dob = fields.Date(string="Date of Birth", tracking=True)
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', tracking=True)
    student_blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        string='Blood Group', tracking=True)
    student_calendar_count = fields.Integer(string="Calendar Count", compute="_compute_student_calendar_count", tracking=True)
    nationality = fields.Many2one('res.country', string='Nationality', tracking=True)
    calendar_ids = fields.One2many('school.calendar', 'student_id', string="Calendars")


    # compute function
    def _compute_student_calendar_count(self):
        # count student_calendar_count
        for record in self:
            student_calendar_count = self.env['school.calendar'].search_count([('student_id','=',record.id)])
            record.student_calendar_count = student_calendar_count

    # override function create
    @api.model
    def create(self, vals):
        # show sequence
        if vals.get('sequence', _('New')) == _('New'):
            # the name inside next_by_code is get by file data/sequence.xml
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.students') or _('New')

        # if not get data from field "name", we will add it by middle_name + last_name
        if not vals.get('name'):
            vals['name'] = vals['middle_name'] + " " + vals['last_name']
        res = super(Students, self).create(vals)
        return res

    # override function copy
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            # add (copy) after name
            default['name'] = _("%s (copy)") % (self.name)
        return super(Students, self).copy(default=default)

    # override function name_get
    # this function work when we click on dropdown which listed the records of this model
    # Ex: create new calendar -> click on students dropdown
    def name_get(self):
        result = []
        for record in self:
            # add sequence before name
            # Ex: [S00001] student 1
            name = '[' + record.sequence + '] ' + record.name
            result.append((record.id, name))
        return result

    @api.constrains('name')
    def check_name(self):
        # check if name exists in db, then throw error
        for record in self:
            # we need the ('id','!=',record.id) because we need to remove current record from the constrain
            # or else, it will always found the record
            # this only happen in contrains
            student = self.env['school.students'].search([('name','=',record.name),('id','!=',record.id)])
            if (student):
                raise ValidationError(_('Name %s already exists', self.name))