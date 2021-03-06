from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ArchiveRepository(models.Model):
    _name = 'archive.repository'

    name = fields.Char(
        required=True,
    )
    file_ids = fields.One2many(
        'archive.file',
        inverse_name='repository_id',
        readonly=True,
    )
    expects_destruction = fields.Boolean(default=False)
    destruction_months = fields.Integer()
    active = fields.Boolean(default=True)
    model_ids = fields.Many2many(
        'ir.model',
    )

    @api.multi
    def toggle_active(self):
        for repository in self.filtered(lambda r: r.active):
            if repository.file_ids.filtered(lambda r: r.active):
                raise ValidationError(_(
                    'Repositories should have no files in order to be archived'
                ))
        return super().toggle_active()
