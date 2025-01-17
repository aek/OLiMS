"""ReferenceSample represents a reference sample used for quality control testing
"""

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from dependencies.dependency import DateTime
# from dependencies.dependency import REFERENCE_CATALOG
# from dependencies.dependency import *
# from dependencies.dependency import HoldingReference
# from dependencies.dependency import permissions
# from dependencies.dependency import WorkflowException
# from dependencies.dependency import View
# from dependencies.dependency import getToolByName
# from dependencies.dependency import _createObjectByType
# from lims import PMF, bikaMessageFactory as _
# from lims.idserver import renameAfterCreation
# from lims.utils import t
# from lims.browser.fields import ReferenceResultsField
# from lims.browser.widgets import DateTimeWidget as bika_DateTimeWidget
# from lims.browser.widgets import ReferenceResultsWidget
# from lims.config import PROJECTNAME
# from lims.content.bikaschema import BikaSchema
# from lims.interfaces import IReferenceSample
# from lims.utils import sortable_title, tmpID
# from lims.utils import to_unicode as _u
# from lims.utils import to_utf8
# from dependencies.dependency import implements
# import sys, time

from lims import bikaMessageFactory as _
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.boolean_field import BooleanField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, BooleanWidget, DateTimeWidget, TextAreaWidget
from openerp import fields, models
from base_olims_model import BaseOLiMSModel
import datetime
REFERENCE_SAMPLE_STATES = (
    ('current','Current'),
    ('expired','Expired'),
    ('disposed','Disposed'),
    )
#schema = BikaSchema.copy() + Schema((
schema = (StringField('Title',
        required = 1,
        widget = StringWidget(
            label=_("Title"),
        ),
    ),
    fields.Char(string="ID",compute="computeReferenceSampleId"),
    fields.Many2one(string='Reference Definition',
                   comodel_name='olims.reference_definition',
        # schemata = 'Description',
        # allowed_types = ('ReferenceDefinition',),
        # relationship = 'ReferenceSampleReferenceDefinition',
        # referenceClass = HoldingReference,
        # vocabulary = "getReferenceDefinitions",
        # widget = ReferenceWidget(
        #     checkbox_bound = 0,
        #     label=_("Reference Definition"),
        # ),
                    ),

    BooleanField('Blank',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Blank"),
            description=_("Reference sample values are zero or 'blank'"),
        ),
    ),
    BooleanField('Hazardous',
        schemata = 'Description',
        default = False,
        widget = BooleanWidget(
            label=_("Hazardous"),
            description=_("Samples of this type should be treated as hazardous"),
        ),
    ),

    fields.Many2one(string='Manufacturer',
                   comodel_name='olims.manufacturer',
        # schemata = 'Description',
        # allowed_types = ('Manufacturer',),
        # relationship = 'ReferenceSampleManufacturer',
        # vocabulary = "getReferenceManufacturers",
        # referenceClass = HoldingReference,
        # widget = ReferenceWidget(
        #     checkbox_bound = 0,
        #     label=_("Manufacturer"),
        # ),
                    ),
    StringField('CatalogueNumber',
        schemata = 'Description',
        widget = StringWidget(
            label=_("Catalogue Number"),
        ),
    ),
    StringField('LotNumber',
        schemata = 'Description',
        widget = StringWidget(
            label=_("Lot Number"),
        ),
    ),
    TextField('Remarks',
        schemata = 'Description',
        searchable = True,
        default_content_type = 'text/plain',
        allowed_content_types= ('text/plain', ),
        default_output_type="text/plain",
        widget = TextAreaWidget(
            macro = "bika_widgets/remarks",
            label=_("Remarks"),
            append_only = True,
        ),
    ),
    DateTimeField('Date Sampled',
        schemata = 'Dates',
        widget = DateTimeWidget(
            label=_("Date Sampled"),
        ),
    ),
    DateTimeField('Date Received',
        schemata = 'Dates',
        default_method = 'current_date',
        widget = DateTimeWidget(
            label=_("Date Received"),
        ),
    ),
    DateTimeField('Date Opened',
        schemata = 'Dates',
        widget = DateTimeWidget(
            label=_("Date Opened"),
        ),
    ),
    DateTimeField('Expiry Date',
        schemata = 'Dates',
        required = 1,
        widget = DateTimeWidget(
            label=_("Expiry Date"),
        ),
    ),
    DateTimeField('DateExpired',
        readonly=True,
        schemata = 'Dates',
        widget = DateTimeWidget(
            label=_("Date Expired"),
            visible = {'edit':'hidden'},
        ),
    ),
    DateTimeField('DateDisposed',
        readonly=True,
        schemata = 'Dates',
        widget = DateTimeWidget(
            label=_("Date Disposed"),
            visible = {'edit':'hidden'},
        ),
    ),
    fields.Selection(string='state',selection=REFERENCE_SAMPLE_STATES,
        default='current',
        select=True,
        required=True, readonly=True,
        copy=False, track_visibility='always'
        ),
    
    # ~~~~~~~ To be implemented ~~~~~~~
    fields.One2many(string='ReferenceResults',
        comodel_name = 'olims.reference_values',
        inverse_name='reference_sample_id',
        required = True,
#         subfield_validators = {
#                     'result':'referencevalues_validator',
#                     'min':'referencevalues_validator',
#                     'max':'referencevalues_validator',
#                     'error':'referencevalues_validator'},
#         widget = ReferenceResultsWidget(
#             label=_("Expected Values"),
#         ),
    ),

    fields.Many2one(string='Supplier',
        comodel_name='olims.supplier',
        required=True
    #     widget = ComputedWidget(
    #         visible = False,
    #     ),
    ),
    # ComputedField('ReferenceDefinitionUID',
    #     expression = 'here.getReferenceDefinition() and here.getReferenceDefinition().UID() or None',
    #     widget = ComputedWidget(
    #         visible = False,
    #     ),
    # ),
)

#schema['title'].schemata = 'Description'

class ReferenceSample(models.Model, BaseOLiMSModel): #BaseFolder
    _name='olims.reference_sample'
    # implements(IReferenceSample)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    def computeReferenceSampleId(self):
        for record in self:
            record.ID = 'QC-0' + str(record.id)

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    #security.declarePublic('current_date')
    def current_date(self):
        return DateTime()

    def getReferenceDefinitions(self):

        def make_title(o):
            # the javascript uses these strings to decide if it should
            # check the blank or hazardous checkboxes when a reference
            # definition is selected (./js/referencesample.js)
            if not o:
                return ''
            title = _u(o.Title())
            if o.getBlank():
                title += " %s" % t(_('(Blank)'))
            if o.getHazardous():
                title += " %s" % t(_('(Hazardous)'))

            return title

        bsc = getToolByName(self, 'bika_setup_catalog')
        defs = [o.getObject() for o in
                bsc(portal_type = 'ReferenceDefinition',
                    inactive_state = 'active')]
        items = [('','')] + [(o.UID(), make_title(o)) for o in defs]
        o = self.getReferenceDefinition()
        it = make_title(o)
        if o and (o.UID(), it) not in items:
            items.append((o.UID(), it))
        items.sort(lambda x,y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    def getReferenceManufacturers(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [('','')] + [(o.UID, o.Title) for o in
                               bsc(portal_type='Manufacturer',
                                   inactive_state = 'active')]
        o = self.getReferenceDefinition()
        if o and o.UID() not in [i[0] for i in items]:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x,y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    #security.declarePublic('getSpecCategories')
    def getSpecCategories(self):
        tool = getToolByName(self, REFERENCE_CATALOG)
        categories = []
        for spec in self.getReferenceResults():
            service = tool.lookupObject(spec['uid'])
            if service.getCategoryUID() not in categories:
                categories.append(service.getCategoryUID())
        return categories

    #security.declarePublic('getResultsRangeDict')
    def getResultsRangeDict(self):
        specs = {}
        for spec in self.getReferenceResults():
            uid = spec['uid']
            specs[uid] = {}
            specs[uid]['result'] = spec['result']
            specs[uid]['min'] = spec.get('min', '')
            specs[uid]['max'] = spec.get('max', '')
            specs[uid]['error'] = 'error' in spec and spec['error'] or 0
        return specs

    #security.declarePublic('getResultsRangeSorted')
    def getResultsRangeSorted(self):
        tool = getToolByName(self, REFERENCE_CATALOG)

        cats = {}
        for spec in self.getReferenceResults():
            service = tool.lookupObject(spec['uid'])
            service_title = service.Title()
            category = service.getCategoryTitle()
            if not cats.has_key(category):
                cats[category] = {}

            cat = cats[category]
            cat[service_title] = {'category': category,
                                  'service': service_title,
                                  'id': service.getId(),
                                  'unit': service.getUnit(),
                                  'result': spec['result'],
                                  'min': spec.get('min', ''),
                                  'max': spec.get('max', ''),
                                  'error': spec['error']}

        cat_keys = cats.keys()
        cat_keys.sort(lambda x, y:cmp(x.lower(), y.lower()))
        sorted_specs = []
        for cat in cat_keys:
            services = cats[cat]
            service_keys = services.keys()
            service_keys.sort(lambda x, y:cmp(x.lower(), y.lower()))
            for service_key in service_keys:
                sorted_specs.append(services[service_key])

        return sorted_specs

    #security.declarePublic('getReferenceAnalyses')
    def getReferenceAnalyses(self):
        """ return all analyses linked to this reference sample """
        return self.objectValues('ReferenceAnalysis')

    #security.declarePublic('getReferenceAnalysesService')
    def getReferenceAnalysesService(self, service_uid):
        """ return all analyses linked to this reference sample for a service """
        analyses = []
        for analysis in self.objectValues('ReferenceAnalysis'):
            if analysis.getServiceUID() == service_uid:
                analyses.append(analysis)
        return analyses

    #security.declarePublic('getReferenceResult')
    def getReferenceResult(self, service_uid):
        """ Return an array [result, min, max, error] with the desired result
            for a specific service.
            If any reference result found, returns None.
            If no value found for result, min, max, error found returns None
            If floatable value, sets the value in array as floatable, otherwise
            sets the raw value for that spec key
            in its array position
        """
        for spec in self.getReferenceResults():
            if spec['uid'] == service_uid:
                found = False
                outrefs = []
                specitems = ['result', 'min', 'max', 'error']
                for item in specitems:
                    if item in spec:
                        try:
                            floatitem = spec[item]
                            outrefs.append(floatitem)
                        except:
                            outrefs.append(spec[item])
                        found = True
                    else:
                        outrefs.append(None)
                return found == True and outrefs or None
        return None

    #security.declarePublic('addReferenceAnalysis')
    def addReferenceAnalysis(self, service_uid, reference_type):
        """ add an analysis to the sample """
        rc = getToolByName(self, REFERENCE_CATALOG)
        service = rc.lookupObject(service_uid)

        analysis = _createObjectByType("ReferenceAnalysis", self, tmpID())
        analysis.unmarkCreationFlag()

        calculation = service.getCalculation()
        interim_fields = calculation and calculation.getInterimFields() or []
        renameAfterCreation(analysis)

        # maxtime = service.getMaxTimeAllowed() and service.getMaxTimeAllowed() \
        #     or {'days':0, 'hours':0, 'minutes':0}
        # starttime = DateTime()
        # max_days = float(maxtime.get('days', 0)) + \
        #          (
        #              (float(maxtime.get('hours', 0)) * 3600 + \
        #               float(maxtime.get('minutes', 0)) * 60)
        #              / 86400
        #          )
        # duetime = starttime + max_days

        analysis.setReferenceType(reference_type)
        analysis.setService(service_uid)
        analysis.setInterimFields(interim_fields)
        return analysis.UID()


    #security.declarePublic('getServices')
    def getServices(self):
        """ get all services for this Sample """
        tool = getToolByName(self, REFERENCE_CATALOG)
        services = []
        for spec in self.getReferenceResults():
            service = tool.lookupObject(spec['uid'])
            services.append(service)
        return services

    #security.declarePublic('getReferenceResultStr')
    def getReferenceResultStr(self, service_uid):
        specstr = ''
        specs = self.getReferenceResult(service_uid)
        if specs:
            # [result, min, max, error]
            if not specs[0]:
                if specs[1] and specs[2]:
                    specstr = '%s - %s' % (specs[1], specs[2])
                elif specs[1]:
                    specstr = '> %s' % (specs[1])
                elif specs[2]:
                    specstr = '< %s' % (specs[2])
            elif specs[0]:
                if specs[3] and specs[3] != 0:
                    specstr = '%s (%s%)' % (specs[0], specs[3])
                else:
                    specstr = specs[0]
        return specstr
    def workflow_script_current(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'current'
        })
        return True
    # XXX workflow methods
    def workflow_script_expire(self,cr,uid,ids,context=None):
        """ expire sample """
        dateexpire = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'expired','DateExpired': dateexpire,
        })
        return True
        # self.setDateExpired(DateTime())
        # self.reindexObject()

    def workflow_script_dispose(self,cr,uid,ids,context=None):
        """ dispose sample """
        datedepose = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'disposed','DateDisposed': datedepose,
        })
        return True
        # self.setDateDisposed(DateTime())
        # self.reindexObject()

#registerType(ReferenceSample, PROJECTNAME)
ReferenceSample.initialze(schema)