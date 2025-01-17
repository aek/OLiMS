# -*- coding: utf-8 -*-
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from dependencies.dependency import DateTime
# from dependencies.dependency import HistoryAwareMixin
# from dependencies.dependency import makeDisplayList
# from dependencies.dependency import RecordField, RecordsField
# from dependencies.dependency import registerField
# from dependencies.dependency import DisplayList, ReferenceField, \
#     ComputedField, ComputedWidget, BooleanField, \
#     BooleanWidget, StringField, SelectionWidget, \
#     FixedPointField, DecimalWidget, IntegerField, \
#     IntegerWidget, StringWidget, BaseContent, \
#     Schema, registerType, MultiSelectionWidget
# from dependencies.dependency import HoldingReference
# from lims.utils import to_unicode as _u
# from lims.browser.widgets.durationwidget import DurationWidget
# from lims.browser.widgets.partitionsetupwidget import PartitionSetupWidget
# from lims.browser.widgets.recordswidget import RecordsWidget
# from lims.browser.widgets.referencewidget import ReferenceWidget
# from lims.browser.fields import *
# from lims.content.bikaschema import BikaSchema
# from magnitude import MagnitudeError
# from OLiMS.dependencies.dependency import i18n
# from dependencies.dependency import implements
# import math
# from lims.interfaces import IAnalysisService
# from dependencies.dependency import RegexValidator
# from lims.config import ATTACHMENT_OPTIONS, PROJECTNAME, \
#     SERVICE_POINT_OF_CAPTURE
# import sys

from dependencies.dependency import DisplayList
from dependencies import transaction
from lims.utils.analysis import get_significant_digits
# from magnitude import mg
from dependencies.dependency import getToolByName
from dependencies.dependency import WorkflowException
from lims import bikaMessageFactory as _
from lims.utils import to_utf8 as _c
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.reference_field import ReferenceField
from fields.boolean_field import BooleanField
from fields.integer_field import IntegerField
from fields.fixed_point_field import FixedPointField
from fields.text_field import TextField
from fields.widget.widget import *
from openerp import fields, models

SERVICE_POINT_OF_CAPTURE =(
                           ('field', _('Field')),
                           ('lab', _('Lab')),
                           )

ATTACHMENT_OPTIONS = (
                      ('r', 'Required'),
                      ('p', 'Permitted'),
                      ('n', 'Not Permitted')
                      )
# ~~~~~~~ To be implemented ~~~~~~~
# def getContainers(instance,
#                   minvol=None,
#                   allow_blank=True,
#                   show_container_types=True,
#                   show_containers=True):
#     """ Containers vocabulary
# 
#     This is a separate class so that it can be called from ajax to filter
#     the container list, as well as being used as the AT field vocabulary.
# 
#     Returns a tuple of tuples: ((object_uid, object_title), ())
# 
#     If the partition is flagged 'Separate', only containers are displayed.
#     If the Separate flag is false, displays container types.
# 
#     XXX bsc = self.portal.bika_setup_catalog
#     XXX obj = bsc(getKeyword='Moist')[0].getObject()
#     XXX u'Container Type: Canvas bag' in obj.getContainers().values()
#     XXX True
# 
#     """
# 
#     bsc = getToolByName(instance, 'bika_setup_catalog')
# 
#     items = allow_blank and [['', _('Any')]] or []
# 
#     containers = []
#     for container in bsc(portal_type='Container', sort_on='sortable_title'):
#         container = container.getObject()
# 
#         # verify container capacity is large enough for required sample volume.
#         if minvol is not None:
#             capacity = container.getCapacity()
#             try:
#                 capacity = capacity.split(' ', 1)
#                 capacity = mg(float(capacity[0]), capacity[1])
#                 if capacity < minvol:
#                     continue
#             except:
#                 # if there's a unit conversion error, allow the container
#                 # to be displayed.
#                 pass
# 
#         containers.append(container)
# 
#     if show_containers:
#         # containers with no containertype first
#         for container in containers:
#             if not container.getContainerType():
#                 items.append((container.UID(), container.Title()))
# 
#     ts = getToolByName(instance, 'translation_service').translate
#     cat_str = _c(ts(_('Container Type')))
#     containertypes = [c.getContainerType() for c in containers]
#     containertypes = dict([(ct.UID(), ct.Title())
#                            for ct in containertypes if ct])
#     for ctype_uid, ctype_title in containertypes.items():
#         ctype_title = _c(ctype_title)
#         if show_container_types:
#             items.append((ctype_uid, "%s: %s" % (cat_str, ctype_title)))
#         if show_containers:
#             for container in containers:
#                 ctype = container.getContainerType()
#                 if ctype and ctype.UID() == ctype_uid:
#                     items.append((container.UID(), container.Title()))
# 
#     items = tuple(items)
#     return items

# ~~~~~~~ To be implemented ~~~~~~~
# class PartitionSetupField(RecordsField):
#     _properties = RecordsField._properties.copy()
#     _properties.update({
#         'subfields': (
#             'sampletype',
#             'separate',
#             'preservation',
#             'container',
#             'vol',
#             # 'retentionperiod',
#         ),
#         'subfield_labels': {
#             'sampletype': _('Sample Type'),
#             'separate': _('Separate Container'),
#             'preservation': _('Preservation'),
#             'container': _('Container'),
#             'vol': _('Required Volume'),
#             # 'retentionperiod': _('Retention Period'),
#         },
#         'subfield_types': {
#             'separate': 'boolean',
#             'vol': 'string',
#             'preservation': 'sampletype',
#             'container': 'selection',
#             'preservation': 'selection',
#         },
#         'subfield_vocabularies': {
#             'sampletype': 'SampleTypes',
#             'preservation': 'Preservations',
#             'container': 'Containers',
#         },
#         'subfield_sizes': {
#             'sampletype': 1,
#             'preservation': 6,
#             'vol': 8,
#             'container': 6,
#             # 'retentionperiod':10,
#         }
#     })
#     security = ClassSecurityInfo()
# 
#     security.declarePublic('SampleTypes')
# 
#     def SampleTypes(self, instance=None):
#         instance = instance or self
#         bsc = getToolByName(instance, 'bika_setup_catalog')
#         items = []
#         for st in bsc(portal_type='SampleType',
#                       inactive_state='active',
#                       sort_on='sortable_title'):
#             st = st.getObject()
#             title = st.Title()
#             items.append((st.UID(), title))
#         items = [['', '']] + list(items)
#         return DisplayList(items)
# 
#     security.declarePublic('Preservations')
# 
#     def Preservations(self, instance=None):
#         instance = instance or self
#         bsc = getToolByName(instance, 'bika_setup_catalog')
#         items = [(c.UID, c.title) for c in
#                  bsc(portal_type='Preservation',
#                      inactive_state='active',
#                      sort_on='sortable_title')]
#         items = [['', _('Any')]] + list(items)
#         return DisplayList(items)
# 
#     security.declarePublic('Containers')
# 
#     def Containers(self, instance=None):
#         instance = instance or self
#         items = getContainers(instance, allow_blank=True)
#         return DisplayList(items)


# registerField(PartitionSetupField, title="", description="")

# # XXX When you modify this schema, be sure to edit the list of fields
## to duplicate, in bika_analysisservices.py.

# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema = BikaSchema.copy() + Schema((
schema = (StringField('Service',
        required=1,
        widget=StringWidget(
            label=_('Title'),
            description=_('Title is required.'),
        ),
    ),
    TextField('Description',
        widget=TextAreaWidget(
            label=_('Description'),
            description=_('Used in item listings and search results.'),
        ),
    ),
    StringField('ShortTitle',
                schemata="Description",
                widget=StringWidget(
                    label = _("Short title"),
                    description=_(
                        "If text is entered here, it is used instead of the " + \
                        "title when the service is listed in column headings. " + \
                        "HTML formatting is allowed.")
                ),
    ),
    BooleanField('ScientificName',
                 schemata="Description",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Scientific name"),
                     description = _(
                        "If enabled, the name of the analysis will be " + \
                        "written in italics."),
                 ),
    ),
    StringField('Unit',
                schemata="Description",
                widget=StringWidget(
                    label = _("Unit"),
                    description=_(
                        "The measurement units for this analysis service' results, " + \
                        "e.g. mg/l, ppm, dB, mV, etc."),
                ),
    ),
    IntegerField('Precision',
                 schemata="Analysis",
                 widget=IntegerWidget(
                     label = _("Precision as number of decimals"),
                     description=_(
                         "Define the number of decimals to be used for this result."),
                 ),
    ),
    IntegerField('ExponentialFormatPrecision',
                 schemata="Analysis",
                 default = 7,
                 widget=IntegerWidget(
                     label = _("Exponential format precision"),
                     description=_(
                         "Define the precision when converting values to exponent " + \
                         "notation.  The default is 7."),
                 ),
    ),
    FixedPointField('LowerDetectionLimit',
                    schemata="Analysis",
                    default='0.0',
                    precision=7,
                    widget=DecimalWidget(
                        label = _("Lower Detection Limit (LDL)"),
                        description = _("The Lower Detection Limit is " + \
                                        "the lowest value to which the " + \
                                        "measured parameter can be " + \
                                        "measured using the specified " + \
                                        "testing methodology. Results " + \
                                        "entered which are less than " + \
                                        "this value will be reported " + \
                                        "as < LDL")
                    ),
    ),
    FixedPointField('UpperDetectionLimit',
                schemata="Analysis",
                default='1000000000.0',
                precision=7,
                widget=DecimalWidget(
                    label = _("Upper Detection Limit (UDL)"),
                    description = _("The Upper Detection Limit is the " + \
                                    "highest value to which the " + \
                                    "measured parameter can be measured " + \
                                    "using the specified testing " + \
                                    "methodology. Results entered " + \
                                    "which are greater than this value " + \
                                    "will be reported as > UDL")
                ),
    ),
    # LIMS-1775 Allow to select LDL or UDL defaults in results with readonly mode
    # https://jira.bikalabs.com/browse/LIMS-1775
    # Some behavior controlled with javascript: If checked, the field
    # "AllowManualDetectionLimit" will be displayed.
    # See browser/js/bika.lims.analysisservice.edit.js
    #
    # Use cases:
    # a) If "DetectionLimitSelector" is enabled and
    # "AllowManualDetectionLimit" is enabled too, then:
    # the analyst will be able to select an '>', '<' operand from the
    # selection list and also set the LD manually.
    #
    # b) If "DetectionLimitSelector" is enabled and
    # "AllowManualDetectionLimit" is unchecked, the analyst will be
    # able to select an operator from the selection list, but not set
    # the LD manually: the default LD will be displayed in the result
    # field as usuall, but in read-only mode.
    #
    # c) If "DetectionLimitSelector" is disabled, no LD selector will be
    # displayed in the results table.
    BooleanField('DetectionLimitSelector',
        schemata="Analysis",
        default=False,
        widget=BooleanWidget(
            label = _("Display a Detection Limit selector"),
            description = _("If checked, a selection list will be " + \
                            "displayed next to the analysis' result " + \
                            "field in results entry views. By using " + \
                            "this selector, the analyst will be able " + \
                            "to set the value as a Detection Limit " + \
                            "(LDL or UDL) instead of a regular result"),
        ),
    ),
    # Behavior controlled with javascript: Only visible when the
    # "DetectionLimitSelector" is checked
    # See browser/js/bika.lims.analysisservice.edit.js
    # Check inline comment for "DetecionLimitSelector" field for
    # further information.
    BooleanField('AllowManualDetectionLimit',
             schemata="Analysis",
             default=False,
             widget=BooleanWidget(
                label = _("Allow Manual Detection Limit input"),
                description = _("Allow the analyst to manually " + \
                                "replace the default Detection Limits " + \
                                "(LDL and UDL) on results entry views"),
             ),
    ),
    BooleanField('ReportDryMatter',
                 schemata="Analysis",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Report as Dry Matter"),
                     description = _("These results can be reported as dry matter"),
                 ),
    ),
    # ~~~~~~~~~~ Using Odoo fields.Selection field due to SelectionWidget ~~~~~~~~~~
    fields.Selection(string='AttachmentOption',
                selection=ATTACHMENT_OPTIONS,
#                 schemata="Analysis",
                default='p',
                help="Indicates whether file attachments, e.g. microscope images, " + \
                        "are required for this analysis and whether file upload function " + \
                        "will be available for it on data capturing screens",
#                 vocabulary=ATTACHMENT_OPTIONS,
#                 widget=SelectionWidget(
#                     label = _("Attachment Option"),
#                     description=_(
#                         "Indicates whether file attachments, e.g. microscope images, "
#                         "are required for this analysis and whether file upload function "
#                         "will be available for it on data capturing screens"),
#                     format='select',
#                 ),
    ),
    StringField('Keyword',
                schemata="Description",
                required=1,
                searchable=True,
                validators=('servicekeywordvalidator'),
                widget=StringWidget(
                    label = _("Analysis Keyword"),
                    description=_(
                        "The unique keyword used to identify the analysis service in " + \
                        "import files of bulk AR requests and results imports from instruments. " + \
                        "It is also used to identify dependent analysis services in user " + \
                        "defined results calculations"),
                ),
    ),
    # Allow/Disallow manual entry of results
    # Behavior controlled by javascript depending on Instruments field:
    # - If InstrumentEntry not checked, set checked and readonly
    # - If InstrumentEntry checked, set as not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('ManualEntryOfResults',
                 schemata="Method",
                 default=True,
                 readonly=True,
                 widget=BooleanWidget(
                     label = _("Allow manual entry of results"),
                     description=_("Select if the results for this Analysis " + \
                                   "Service can be set manually."),
                 )
    ),
    # Allow/Disallow instrument entry of results
    # Behavior controlled by javascript depending on Instruments field:
    # - If no instruments available, hide and uncheck
    # - If at least one instrument selected, checked, but not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('InstrumentEntryOfResults',
                 schemata="Method",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Allow instrument entry of results"),
                     description=_("Select if the results for this Analysis " + \
                                   "Service can be set using an Instrument."),
                 )
    ),
    # Instruments associated to the AS
    # List of instruments capable to perform the Analysis Service. The
    # Instruments selected here are displayed in the Analysis Request
    # Add view, closer to this Analysis Service if selected.
    # - If InstrumentEntry not checked, hide and unset
    # - If InstrumentEntry checked, set the first selected and show
    fields.Many2many(string='Instruments',
                   comodel_name='olims.instrument',
#                    schemata="Method",
                   required=False,
                   help="More than one instrument can do an " + \
                                    "Analysis Service. The instruments " + \
                                    "selected here are displayed in the " + \
                                    "Analysis Request creation view for its " + \
                                    "selection when this Analysis Service is " + \
                                    "selected.",
#                    multiValued=1,
#                    vocabulary_display_path_bound=sys.maxint,
#                    vocabulary='_getAvailableInstrumentsDisplayList',
#                    allowed_types=('Instrument',),
#                    relationship='AnalysisServiceInstruments',
#                    referenceClass=HoldingReference,
#                    widget=MultiSelectionWidget(
#                        label = _("Instruments"),
#                        description=_("More than one instrument can do an " + \
#                                      "Analysis Service. The instruments " + \
#                                      "selected here are displayed in the " + \
#                                      "Analysis Request creation view for its " + \
#                                      "selection when this Analysis Service is " + \
#                                      "selected."),
#                    )
    ),
    # Default instrument to be used.
    # Gets populated with the instruments selected in the multiselection
    # box above.
    # Behavior controlled by js depending on ManualEntry/Instruments:
    # - Populate dynamically with selected Instruments
    # - If InstrumentEntry checked, set first selected instrument
    # - If InstrumentEntry not checked, hide and set None
    # See browser/js/bika.lims.analysisservice.edit.js
    
    fields.Many2one(string='Instrument',
                    comodel_name='olims.instrument',
#                    schemata="Method",
#                    searchable=True,
                    required=False,
# #                 vocabulary_display_path_bound=sys.maxint,
#                   vocabulary='_getAvailableInstrumentsDisplayList',
#                   allowed_types=('Instrument',),
#                   relationship='AnalysisServiceInstrument',
#                   referenceClass=HoldingReference,
#                   widget=SelectionWidget(
#                       format='select',
#                       label = _("Default Instrument"),
#                   ),
    ),
    # Returns the Default's instrument title. If no default instrument
    # set, returns string.empty
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('InstrumentTitle',
#                   expression="context.getInstrument() and context.getInstrument().Title() or ''",
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),
    # Manual methods associated to the AS
    # List of methods capable to perform the Analysis Service. The
    # Methods selected here are displayed in the Analysis Request
    # Add view, closer to this Analysis Service if selected.
    # Use getAvailableMethods() to retrieve the list with methods both
    # from selected instruments and manually entered.
    # Behavior controlled by js depending on ManualEntry/Instrument:
    # - If InsrtumentEntry not checked, show
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2many(string='Methods',
        comodel_name='olims.method',
        help="The Analysis Service can be performed by " + \
                            "using more than one Method. The methods " + \
                            "selected here are displayed in the " + \
                            "Analysis Request creation view for its " + \
                            "selection when this Analaysis Service " + \
                            "is selected. Only methods with 'Allow " + \
                            "manual entry of results' enabled are " + \
                            "displayed.",
#         schemata = "Method",
        required = False,
#         multiValued = 1,
#         vocabulary_display_path_bound = sys.maxint,
#         vocabulary = '_getAvailableMethodsDisplayList',
#         allowed_types = ('Method',),
#         relationship = 'AnalysisServiceMethods',
#         referenceClass = HoldingReference,
#         widget = MultiSelectionWidget(
#             label = _("Methods"),
#             description = _("The Analysis Service can be performed by " + \
#                             "using more than one Method. The methods " + \
#                             "selected here are displayed in the " + \
#                             "Analysis Request creation view for its " + \
#                             "selection when this Analaysis Service " + \
#                             "is selected. Only methods with 'Allow " + \
#                             "manual entry of results' enabled are " + \
#                             "displayed."),
#         )
    ),
    # Default method to be used. This field is used in Analysis Service
    # Edit view, use getMethod() to retrieve the Method to be used in
    # this Analysis Service.
    # Gets populated with the methods selected in the multiselection
    # box above or with the default instrument's method.
    # Behavior controlled by js depending on ManualEntry/Instrument/Methods:
    # - If InstrumentEntry checked, set instrument's default method, and readonly
    # - If InstrumentEntry not checked, populate dynamically with
    #   selected Methods, set the first method selected and non-readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2one(string='_Method',
        comodel_name='olims.method',
#         schemata = "Method",
        required = 0,
        help="If 'Allow instrument entry of results' " + \
                        "is selected, the method from the default instrument " + \
                        "will be used. Otherwise, only the methods " + \
                        "selected above will be displayed.",
#         searchable = True,
#         vocabulary_display_path_bound = sys.maxint,
#         allowed_types = ('Method',),
#         vocabulary = '_getAvailableMethodsDisplayList',
#         relationship = 'AnalysisServiceMethod',
#         referenceClass = HoldingReference,
#         widget = SelectionWidget(
#             format='select',
#             label = _("Default Method"),
#             description=_("If 'Allow instrument entry of results' " + \
#                           "is selected, the method from the default instrument " + \
#                           "will be used. Otherwise, only the methods " + \
#                           "selected above will be displayed.")
#         ),
    ),
    # Allow/Disallow to set the calculation manually
    # Behavior controlled by javascript depending on Instruments field:
    # - If no instruments available, hide and uncheck
    # - If at least one instrument selected, checked, but not readonly
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('UseDefaultCalculation',
                 schemata="Method",
                 default=True,
                 widget=BooleanWidget(
                     label = _("Use default calculation"),
                     description=_("Select if the calculation to be used is the " + \
                                   "calculation set by default in the default " + \
                                   "method. If unselected, the calculation can " + \
                                   "be selected manually"),
                 )
    ),
    # Default calculation to be used. This field is used in Analysis Service
    # Edit view, use getCalculation() to retrieve the Calculation to be used in
    # this Analysis Service.
    # The default calculation is the one linked to the default method
    # Behavior controlled by js depending on UseDefaultCalculation:
    # - If UseDefaultCalculation is set to False, show this field
    # - If UseDefaultCalculation is set to True, show this field
    # See browser/js/bika.lims.analysisservice.edit.js
    fields.Many2one(string='_Calculation',
                   comodel_name='olims.calculation',
#                    schemata="Method",
                   required=False,
                   help="Default calculation to be used from the " + \
                                    "default Method selected. The Calculation " + \
                                    "for a method can be assigned in the Method " + \
                                    "edit view.",
#                    vocabulary_display_path_bound=sys.maxint,
#                    vocabulary='_getAvailableCalculationsDisplayList',
#                    allowed_types=('Calculation',),
#                    relationship='AnalysisServiceCalculation',
#                    referenceClass=HoldingReference,
#                    widget=SelectionWidget(
#                        format='select',
#                        label = _("Default Calculation"),
#                        description=_("Default calculation to be used from the " + \
#                                      "default Method selected. The Calculation " + \
#                                      "for a method can be assigned in the Method " + \
#                                      "edit view."),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
    # Default calculation is not longer linked directly to the AS: it
    # currently uses the calculation linked to the default Method.
    # Use getCalculation() to retrieve the Calculation to be used.
    # Old ASes (before 3008 upgrade) can be linked to the same Method,
    # but to different Calculation objects. In that case, the Calculation
    # is saved as DeferredCalculation and UseDefaultCalculation is set to
    # False in the upgrade.
    # Behavior controlled by js depending on UseDefaultCalculation:
    # - If UseDefaultCalculation is set to False, show this field
    # - If UseDefaultCalculation is set to True, show this field
    # See browser/js/bika.lims.analysisservice.edit.js
    #     bika/lims/upgrade/to3008.py
    fields.Many2one(string='DeferredCalculation',
                   comodel_name='olims.calculation',
#                    schemata="Method",
                   required=False,
                   help="If required, select a calculation for the analysis here. " + \
                            "Calculations can be configured under the calculations item " + \
                            "in the LIMS set-up",
#                    vocabulary_display_path_bound=sys.maxint,
#                    vocabulary='_getAvailableCalculationsDisplayList',
#                    allowed_types=('Calculation',),
#                    relationship='AnalysisServiceDeferredCalculation',
#                    referenceClass=HoldingReference,
#                    widget=SelectionWidget(
#                        format='select',
#                        label = _("Alternative Calculation"),
#                        description=_(
#                            "If required, select a calculation for the analysis here. "
#                            "Calculations can be configured under the calculations item "
#                            "in the LIMS set-up"),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('CalculationTitle',
#                   expression="context.getCalculation() and context.getCalculation().Title() or ''",
#                   searchable=True,
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('CalculationUID',
#                   expression="context.getCalculation() and context.getCalculation().UID() or ''",
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),

    fields.Many2many(string='InterimFields',
                    comodel_name='olims.interimfield',
                          #        schemata='Method',
#                        widget=RecordsWidget(
#                            label = _("Calculation Interim Fields"),
#                            description=_(
#                                "Values can be entered here which will override the defaults "
#                                "specified in the Calculation Interim Fields."),
#                        )
),


    
    fields.Char(string='Days', required=True),
    fields.Char(string='Hours', required=True),
    fields.Char(string='Minutes', required=True),
    
    
    FixedPointField('DuplicateVariation',
                    schemata="Method",
                    widget=DecimalWidget(
                        label = _("Duplicate Variation %"),
                        description=_(
                            "When the results of duplicate analyses on worksheets, " + \
                            "carried out on the same sample, differ with more than " + \
                            "this percentage, an alert is raised"),
                    ),
    ),
    BooleanField('Accredited',
                 schemata="Method",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Accredited"),
                     description=_(
                         "Check this box if the analysis service is included in the " + \
                         "laboratory's schedule of accredited analyses"),
                 ),
    ),
    
    fields.Selection(string='PointOfCapture',
                selection=SERVICE_POINT_OF_CAPTURE,
#                 schemata="Description",
                required=1,
                default='lab',
                help="The results of field analyses are captured during sampling " + \
                        "at the sample point, e.g. the temperature of a water sample " + \
                        "in the river where it is sampled. Lab analyses are done in " + \
                        "the laboratory",
#                 vocabulary=SERVICE_POINT_OF_CAPTURE,
#                 widget=SelectionWidget(
#                     format='flex',
#                     label = _("Point of Capture"),
#                     description=_(
#                         "The results of field analyses are captured during sampling "
#                         "at the sample point, e.g. the temperature of a water sample "
#                         "in the river where it is sampled. Lab analyses are done in "
#                         "the laboratory"),
#                 ),
    ),
    fields.Many2one(string='category',
                   comodel_name='olims.analysis_category',
#                    schemata="Description",
                   required=True,
                   help="The category the analysis service belongs to",
#                    vocabulary_display_path_bound=sys.maxint,
#                    allowed_types=('AnalysisCategory',),
#                    relationship='AnalysisServiceAnalysisCategory',
#                    referenceClass=HoldingReference,
#                    vocabulary='getAnalysisCategories',
#                    widget=ReferenceWidget(
#                        checkbox_bound=0,
#                        label = _("Analysis Category"),
#                        description=_(
#                            "The category the analysis service belongs to"),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
    FixedPointField('Price',
                    schemata="Description",
                    default='0.00',
                    widget=DecimalWidget(
                        label = _("Price (excluding VAT)"),
                    ),
    ),
    # read access permission
    FixedPointField('BulkPrice',
                    schemata="Description",
                    default='0.00',
                    widget=DecimalWidget(
                        label = _("Bulk price (excluding VAT)"),
                        description=_(
                            "The price charged per analysis for clients who qualify for bulk discounts"),
                    ),
    ),
    fields.Float(compute='computeVATAmount',string='VATAmount'),
    
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('VATAmount',
#                   schemata="Description",
#                   expression='context.getVATAmount()',
#                   widget=ComputedWidget(
#                       label = _("VAT"),
#                       visible={'edit': 'hidden', }
#                   ),
#     ),
fields.Float(compute='computeTotalPrice',string='TotalPrice'),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('TotalPrice',
#                   schemata="Description",
#                   expression='context.getTotalPrice()',
#                   widget=ComputedWidget(
#                       label = _("Total price"),
#                       visible={'edit': 'hidden', }
#                   ),
#     ),
    FixedPointField('VAT',
                    schemata="Description",
                    default_method='getDefaultVAT',
                    widget=DecimalWidget(
                        label = _("VAT %"),
                        description = _("Enter percentage value eg. 14.0"),
                    ),
    ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('CategoryTitle',
#                   expression="context.getCategory() and context.getCategory().Title() or ''",
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),
#     ComputedField('CategoryUID',
#                   expression="context.getCategory() and context.getCategory().UID() or ''",
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),
    fields.Many2one(string='Department',
                   comodel_name='olims.department',
#                    schemata="Description",
                   required=False,
                   help="The laboratory department",
#                    vocabulary_display_path_bound=sys.maxint,
#                    allowed_types=('Department',),
#                    vocabulary='getDepartments',
#                    relationship='AnalysisServiceDepartment',
#                    referenceClass=HoldingReference,
#                    widget=ReferenceWidget(
#                        checkbox_bound=0,
#                        label = _("Department"),
#                        description = _("The laboratory department"),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
# ~~~~~~~ To be implemented ~~~~~~~
#     ComputedField('DepartmentTitle',
#                   expression="context.getDepartment() and context.getDepartment().Title() or ''",
#                   searchable=True,
#                   widget=ComputedWidget(
#                       visible=False,
#                   ),
#     ),

# 
fields.One2many(string='Uncertainties',
                       comodel_name='olims.uncertinty_service',
                       inverse_name='analysis_service_id'
        ),


    # Calculate the precision from Uncertainty value
    # Behavior controlled by javascript
    # - If checked, Precision and ExponentialFormatPrecision are not displayed.
    #   The precision will be calculated according to the uncertainty.
    # - If checked, Precision and ExponentialFormatPrecision will be displayed.
    # See browser/js/bika.lims.analysisservice.edit.js
    BooleanField('PrecisionFromUncertainty',
                 schemata="Uncertainties",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Calculate Precision from Uncertainties"),
                     description=_("Precision as the number of significant " + \
                                   "digits according to the uncertainty. " + \
                                   "The decimal position will be given by " + \
                                   "the first number different from zero in " + \
                                   "the uncertainty, at that position the " + \
                                   "system will round up the uncertainty " + \
                                   "and results. " + \
                                   "For example, with a result of 5.243 and " + \
                                   "an uncertainty of 0.22, the system " + \
                                   "will display correctly as 5.2+-0.2. " + \
                                   "If no uncertainty range is set for the " + \
                                   "result, the system will use the " + \
                                   "fixed precision set."),
                 ),
    ),

    # If checked, an additional input with the default uncertainty will
    # be displayed in the manage results view. The value set by the user
    # in this field will override the default uncertainty for the analysis
    # result
    BooleanField('AllowManualUncertainty',
                 schemata="Uncertainties",
                 default=False,
                 widget=BooleanWidget(
                    label = _("Allow manual uncertainty value input"),
                    description = _("Allow the analyst to manually " + \
                                    "replace the default uncertainty " + \
                                    "value."),
                ),
    ),
          
          
          fields.One2many(string='ResultOptions',
                       comodel_name='olims.result_option',
                       inverse_name='service_resultoption_id'

        ),

    BooleanField('Separate',
                 schemata='Container and Preservation',
                 default=False,
                 required=0,
                 widget=BooleanWidget(
                     label = _("Separate Container"),
                     description=_("Check this box to ensure a separate sample " + \
                                   "container is used for this analysis service"),
                 ),
    ),

    fields.Many2one(string='Preservation',
                    comodel_name='olims.preservation',
                    help="Select a default preservation for this " + \
                                    "analysis service. If the preservation depends on " + \
                                    "the sample type combination, specify a preservation " + \
                                    "per sample type in the table below",
                    required=False,
#                    schemata='Container and Preservation',
#                    allowed_types=('Preservation',),
#                    relationship='AnalysisServicePreservation',
#                    referenceClass=HoldingReference,
#                    vocabulary='getPreservations',
#                    multiValued=0,
#                    widget=ReferenceWidget(
#                        checkbox_bound=0,
#                        label = _("Default Preservation"),
#                        description=_("Select a default preservation for this " + \
#                                      "analysis service. If the preservation depends on " + \
#                                      "the sample type combination, specify a preservation " + \
#                                      "per sample type in the table below"),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
    fields.Many2one(string='Container',
                   comodel_name='olims.container',
                   required=False,
                   help="Select the default container to be used for this " + \
                            "analysis service. If the container to be used " + \
                            "depends on the sample type and preservation " + \
                            "combination, specify the container in the sample " + \
                            "type table below",                  
#                    schemata='Container and Preservation',
#                    allowed_types=('Container', 'ContainerType'),
#                    relationship='AnalysisServiceContainer',
#                    referenceClass=HoldingReference,
#                    vocabulary='getContainers',

#                    multiValued=0,
#                    widget=ReferenceWidget(
#                        checkbox_bound=0,
#                        label = _("Default Container"),
#                        description=_(
#                            "Select the default container to be used for this "
#                            "analysis service. If the container to be used "
#                            "depends on the sample type and preservation "
#                            "combination, specify the container in the sample "
#                            "type table below"),
#                        catalog_name='bika_setup_catalog',
#                        base_query={'inactive_state': 'active'},
#                    ),
    ),
    fields.Many2many(string='PartitionSetup', comodel_name='olims.partition_setup'
                           #                         schemata='Container and Preservation',
#                         widget=PartitionSetupWidget(
#                             label=PMF("Preservation per sample type"),
#                             description=_(
#                                 "Please specify preservations that differ from the "
#                                 "analysis service's default preservation per sample "
#                                 "type here."),
                           ),

    BooleanField('Hidden',
                 schemata="Analysis",
                 default=False,
                 widget=BooleanWidget(
                     label = _("Hidden"),
                     description = _(
                        "If enabled, this analysis and its results " + \
                        "will not be displayed by default in reports. " + \
                        "This setting can be overrided in Analysis " + \
                        "Profile and/or Analysis Request"),
                 ),
    ),
    StringField('CommercialID',
        searchable=1,
        schemata='Description',
        required=0,
        widget=StringWidget(
            label=_("Commercial ID"),
            description=_("The service's commercial ID for accounting purposes")
        ),
    ),
    StringField('ProtocolID',
        searchable=1,
        schemata = 'Description',
        required=0,
        widget=StringWidget(
            label=_("Protocol ID"),
            description=_("The service's analytical protocol ID")
        ),
    ),
    StringField('ChangeNote',
        schemata = 'Description',
        widget=StringWidget(
            label=_("Change Note"),
            description=_("Enter a comment that describes the changes you made")
        ),
    ),
)#)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# schema['id'].widget.visible = False
# schema['description'].schemata = 'Description'
# schema['description'].widget.visible = True
# schema['title'].required = True
# schema['title'].widget.visible = True
# schema['title'].schemata = 'Description'
# schema.moveField('ShortTitle', after='title')
# schema.moveField('CommercialID', after='ShortTitle')
# schema.moveField('ProtocolID', after='CommercialID')


class AnalysisService(models.Model, BaseOLiMSModel):#(BaseContent, HistoryAwareMixin):
    _name = 'olims.analysis_service'
    _rec_name = 'Service'
    # marked Keyword field "unique" 
    _sql_constraints = [
        ('uniq_Keyword', 'unique(Keyword)', "The unique keyword used to identify the analysis service."),
    ]
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
#     security = ClassSecurityInfo()
#     schema = schema
#     displayContentsTab = False
#     implements(IAnalysisService)

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation

        return renameAfterCreation(self)

    def Title(self):
        return _c(self.title)

#     security.declarePublic('getDiscountedPrice')

    def getDiscountedPrice(self):
        """ compute discounted price excl. vat """
        price = self.getPrice()
        price = price and price or 0
        discount = self.bika_setup.getMemberDiscount()
        discount = discount and discount or 0
        return float(price) - (float(price) * float(discount)) / 100

#     security.declarePublic('getDiscountedBulkPrice')

    def getDiscountedBulkPrice(self):
        """ compute discounted bulk discount excl. vat """
        price = self.getBulkPrice()
        price = price and price or 0
        discount = self.bika_setup.getMemberDiscount()
        discount = discount and discount or 0
        return float(price) - (float(price) * float(discount)) / 100

    
    def computeTotalPrice(self):
        """ compute total price """
        for record in self:
            price = record.getPrice()
            vat = record.getVAT()
            price = price and price or 0
            vat = vat and vat or 0
            record.TotalPrice = float(price) + (float(price) * float(vat)) / 100
    
    def getTotalPrice(self):
        """ compute total price """
        price = self.getPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    def getTotalBulkPrice(self):
        """ compute total price """
        price = self.getBulkPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

#     security.declarePublic('getTotalDiscountedPrice')

    def getTotalDiscountedPrice(self):
        """ compute total discounted price """
        price = self.getDiscountedPrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

#     security.declarePublic('getTotalDiscountedCorporatePrice')

    def getTotalDiscountedBulkPrice(self):
        """ compute total discounted corporate price """
        price = self.getDiscountedCorporatePrice()
        vat = self.getVAT()
        price = price and price or 0
        vat = vat and vat or 0
        return float(price) + (float(price) * float(vat)) / 100

    def getDefaultVAT(self):
        """ return default VAT from bika_setup """
        try:
            vat = self.bika_setup.getVAT()
            return vat
        except ValueError:
            return "0.00"

#     security.declarePublic('getVATAmount')
    
    def computeVATAmount(self):
        for record in self:
            price, vat = record.getPrice(), record.getVAT()
            record.VATAmount = (float(price) * (float(vat) / 100))
        
#     def getVATAmount(self):
#         """ Compute VATAmount
#         """
#         price, vat = self.getPrice(), self.getVAT()
#         return (float(price) * (float(vat) / 100))

    def getAnalysisCategories(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(o.UID, o.Title) for o in
                 bsc(portal_type='AnalysisCategory',
                     inactive_state='active')]
        o = self.getCategory()
        if o and o.UID() not in [i[0] for i in items]:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x, y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    def _getAvailableInstrumentsDisplayList(self):
        """ Returns a DisplayList with the available Instruments
            registered in Bika-Setup. Only active Instruments are
            fetched. Used to fill the Instruments MultiSelectionWidget
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(i.UID, i.Title) \
                 for i in bsc(portal_type='Instrument',
                              inactive_state='active')]
        items.sort(lambda x, y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    def _getAvailableMethodsDisplayList(self):
        """ Returns a DisplayList with the available Methods
            registered in Bika-Setup. Only active Methods and those
            with Manual Entry field active are fetched.
            Used to fill the Methods MultiSelectionWidget when 'Allow
            Instrument Entry of Results is not selected'.
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(i.UID, i.Title) \
                 for i in bsc(portal_type='Method',
                              inactive_state='active') \
                 if i.getObject().isManualEntryOfResults()]
        items.sort(lambda x, y: cmp(x[1], y[1]))
        items.insert(0, ('', _("None")))
        return DisplayList(list(items))

    def _getAvailableCalculationsDisplayList(self):
        """ Returns a DisplayList with the available Calculations
            registered in Bika-Setup. Only active Calculations are
            fetched. Used to fill the _Calculation and DeferredCalculation
            List fields
        """
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(i.UID, i.Title) \
                 for i in bsc(portal_type='Calculation',
                              inactive_state='active')]
        items.sort(lambda x, y: cmp(x[1], y[1]))
        items.insert(0, ('', _("None")))
        return DisplayList(list(items))

    def getCalculation(self):
        """ Returns the calculation to be used in this AS.
            If UseDefaultCalculation() is set, returns the calculation
            from the default method selected or none (if method hasn't
            defined any calculation). If UseDefaultCalculation is set
            to false, returns the Deferred Calculation (manually set)
        """
        if self.getUseDefaultCalculation():
            return self.getMethod().getCalculation() \
                if (self.getMethod() \
                    and self.getMethod().getCalculation()) \
                else None
        else:
            return self.getDeferredCalculation()

    def getMethod(self):
        """ Returns the method assigned by default to the AS.
            If Instrument Entry Of Results selected, returns the method
            from the Default Instrument or None.
            If Instrument Entry of Results is not selected, returns the
            method assigned directly by the user using the _Method Field
        """
        method = None
        if (self.getInstrumentEntryOfResults() == True):
            method = self.getInstrument().getMethod() \
                if (self.getInstrument() \
                    and self.getInstrument().getMethod()) \
                else None
        else:
            method = self.get_Method();
        return method

    def getAvailableMethods(self):
        """ Returns the methods available for this analysis.
            If the service has the getInstrumentEntryOfResults(), returns
            the methods available from the instruments capable to perform
            the service, as well as the methods set manually for the
            analysis on its edit view. If getInstrumentEntryOfResults()
            is unset, only the methods assigned manually to that service
            are returned.
        """
        methods = self.getMethods()
        muids = [m.UID() for m in methods]
        if self.getInstrumentEntryOfResults() == True:
            # Add the methods from the instruments capable to perform
            # this analysis service
            for ins in self.getInstruments():
                method = ins.getMethod()
                if method and method.UID() not in muids:
                    methods.append(method)
                    muids.append(method.UID())

        return methods

    def getAvailableInstruments(self):
        """ Returns the instruments available for this analysis.
            If the service has the getInstrumentEntryOfResults(), returns
            the instruments capable to perform this service. Otherwhise,
            returns an empty list.
        """
        instruments = self.getInstruments() \
            if self.getInstrumentEntryOfResults() == True \
            else None
        return instruments if instruments else []

    def getDepartments(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [('', '')] + [(o.UID, o.Title) for o in
                              bsc(portal_type='Department',
                                  inactive_state='active')]
        o = self.getDepartment()
        if o and o.UID() not in [i[0] for i in items]:
            items.append((o.UID(), o.Title()))
        items.sort(lambda x, y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    def getUncertainty(self, result=None):
        """
        Return the uncertainty value, if the result falls within
        specified ranges for this service.
        """

        if result is None:
            return None

        uncertainties = self.getUncertainties()
        if uncertainties:
            try:
                result = float(result)
            except ValueError:
                # if analysis result is not a number, then we assume in range
                return None

            for d in uncertainties:
                if float(d['intercept_min']) <= result <= float(
                        d['intercept_max']):
                    unc = 0
                    if str(d['errorvalue']).strip().endswith('%'):
                        try:
                            percvalue = float(d['errorvalue'].replace('%', ''))
                        except ValueError:
                            return None
                        unc = result / 100 * percvalue
                    else:
                        unc = float(d['errorvalue'])

                    return unc
        return None

    def getLowerDetectionLimit(self):
        """ Returns the Lower Detection Limit for this service as a
            floatable
        """
        ldl = self.Schema().getField('LowerDetectionLimit').get(self)
        try:
            return float(ldl)
        except ValueError:
            return 0

    def getUpperDetectionLimit(self):
        """ Returns the Upper Detection Limit for this service as a
            floatable
        """
        udl = self.Schema().getField('UpperDetectionLimit').get(self)
        try:
            return float(udl)
        except ValueError:
            return 0

    def getPrecision(self, result=None):
        """
        Returns the precision for the Analysis Service. If the
        option Calculate Precision according to Uncertainty is not
        set, the method will return the precision value set in the
        Schema. Otherwise, will calculate the precision value
        according to the Uncertainty and the result.
        If Calculate Precision to Uncertainty is set but no result
        provided neither uncertainty values are set, returns the
        fixed precision.

        Examples:
        Uncertainty     Returns
        0               1
        0.22            1
        1.34            0
        0.0021          3
        0.013           2

        For further details, visit
        https://jira.bikalabs.com/browse/LIMS-1334

        :param result: if provided and "Calculate Precision according
                       to the Uncertainty" is set, the result will be
                       used to retrieve the uncertainty from which the
                       precision must be calculated. Otherwise, the
                       fixed-precision will be used.
        :return: the precision
        """
        if self.getPrecisionFromUncertainty() == False:
            return self.Schema().getField('Precision').get(self)
        else:
            uncertainty = self.getUncertainty(result);
            if uncertainty is None:
                return self.Schema().getField('Precision').get(self);

            # Calculate precision according to uncertainty
            # https://jira.bikalabs.com/browse/LIMS-1334
            if uncertainty == 0:
                return 1
            return abs(get_significant_digits(uncertainty))
        return None


    def getExponentialFormatPrecision(self, result=None):
        """
        Returns the precision for the Analysis Service and result
        provided. Results with a precision value above this exponential
        format precision should be formatted as scientific notation.

        If the Calculate Precision according to Uncertainty is not set,
        the method will return the exponential precision value set in
        the Schema. Otherwise, will calculate the precision value
        according to the Uncertainty and the result.

        If Calculate Precision from the Uncertainty is set but no
        result provided neither uncertainty values are set, returns the
        fixed exponential precision.

        Will return positive values if the result is below 0 and will
        return 0 or positive values if the result is above 0.

        Given an analysis service with fixed exponential format
        precision of 4:
        Result      Uncertainty     Returns
        5.234           0.22           0
        13.5            1.34           1
        0.0077          0.008         -3
        32092           0.81           4
        456021          423            5

        For further details, visit
        https://jira.bikalabs.com/browse/LIMS-1334

        :param result: if provided and "Calculate Precision according
                       to the Uncertainty" is set, the result will be
                       used to retrieve the uncertainty from which the
                       precision must be calculated. Otherwise, the
                       fixed-precision will be used.
        :return: the precision
        """
        if not result or self.getPrecisionFromUncertainty() == False:
            return self.Schema().getField('ExponentialFormatPrecision').get(self)
        else:
            uncertainty = self.getUncertainty(result)
            if uncertainty is None:
                return self.Schema().getField('ExponentialFormatPrecision').get(self);

            try:
                result = float(result)
            except ValueError:
                # if analysis result is not a number, then we assume in range
                return self.Schema().getField('ExponentialFormatPrecision').get(self)

            return get_significant_digits(uncertainty)


#     security.declarePublic('getContainers')
# ~~~~~~~ To be implemented ~~~~~~~
#     def getContainers(self, instance=None):
#         # On first render, the containers must be filtered
#         instance = instance or self
#         separate = self.getSeparate()
#         containers = getContainers(instance,
#                                    allow_blank=True,
#                                    show_container_types=not separate,
#                                    show_containers=separate)
#         return DisplayList(containers)

    def getPreservations(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        items = [(o.UID, o.Title) for o in
                 bsc(portal_type='Preservation', inactive_state='active')]
        items.sort(lambda x, y: cmp(x[1], y[1]))
        return DisplayList(list(items))

    def workflow_script_activate(self):
        workflow = getToolByName(self, 'portal_workflow')
        pu = getToolByName(self, 'plone_utils')
        # A service cannot be activated if it's calculation is inactive
        calc = self.getCalculation()
        if calc and \
                        workflow.getInfoFor(calc, "inactive_state") == "inactive":
            message = _("This Analysis Service cannot be activated "
                        "because it's calculation is inactive.")
            pu.addPortalMessage(message, 'error')
            transaction.get().abort()
            raise WorkflowException

    def workflow_scipt_deactivate(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        pu = getToolByName(self, 'plone_utils')
        # A service cannot be deactivated if "active" calculations list it
        # as a dependency.
        active_calcs = bsc(portal_type='Calculation', inactive_state="active")
        calculations = (c.getObject() for c in active_calcs)
        for calc in calculations:
            deps = [dep.UID() for dep in calc.getDependentServices()]
            if self.UID() in deps:
                message = _("This Analysis Service cannot be deactivated "
                            "because one or more active calculations list "
                            "it as a dependency")
                pu.addPortalMessage(message, 'error')
                transaction.get().abort()
                raise WorkflowException

AnalysisService.initialze(schema)
# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# registerType(AnalysisService, PROJECTNAME)
