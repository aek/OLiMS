from openerp import fields, models
from base_olims_model import BaseOLiMSModel

schema = (fields.Many2one(string='Service',
                comodel_name='olims.analysis_service',
#                 relation='analysis_service_specification'
    ),
    fields.Integer('Min'),
    fields.Integer('Max'),
    fields.Integer('Permitted Error'),
)

class Specifications(models.Model, BaseOLiMSModel):
    _name = "olims.specification"
    
Specifications.initialze(schema)