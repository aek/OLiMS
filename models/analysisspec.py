"""Analysis result range specifications for a client
"""

# from dependencies.dependency import *

from dependencies.dependency import getToolByName
from lims import PMF, bikaMessageFactory as _
from openerp import fields, models

from dependencies.dependency import translate
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.widget.widget import TextAreaWidget



#schema = Schema((
# ~~~~~~~ To be implemented ~~~~~~~
#     HistoryAwareReferenceField('SampleType',
#         # schemata = 'Description',
#         # required = 1,
#         vocabulary = "getSampleTypes",
#         vocabulary_display_path_bound = sys.maxint,
#         allowed_types = ('SampleType',),
#         relationship = 'AnalysisSpecSampleType',
#         referenceClass = HoldingReference,
#         widget = ReferenceWidget(
#             checkbox_bound = 0,
#             label = _("Sample Type"),
#         ),
#     ),
#     ComputedField('SampleTypeTitle',
#         expression = "context.getSampleType().Title() if context.getSampleType() else ''",
#         widget = ComputedWidget(
#             visible = False,
#         ),
#     ),
#     ComputedField('SampleTypeUID',
#         expression = "context.getSampleType().UID() if context.getSampleType() else ''",
#         widget = ComputedWidget(
#             visible = False,
#         ),
#     ),
# )) + \
# BikaSchema.copy() + \
# Schema((
schema = (fields.Many2one(string='Sample Type',
                   comodel_name='olims.sample_type',
                   required=False,
                   help="Sample Type",
            ),
    StringField('Title',
              required=1,        
    ),
    TextField('Description',
                widget=TextAreaWidget(
                    description = _('Used in item listings and search results.'),
                            )
    ),
    fields.Many2many(string='Specifications',
                comodel_name='olims.specification',
                relation='analysis_service_specification'
    ),

    #     RecordsField('ResultsRange',
    #     # schemata = 'Specifications',
    #     required = 1,
    #     type = 'analysisspec',
    #     subfields = ('keyword', 'min', 'max', 'error', 'hidemin', 'hidemax',
    #                  'rangecomment'),
    #     required_subfields = ('keyword', 'error'),
    #     subfield_validators = {'min':'analysisspecs_validator',
    #                            'max':'analysisspecs_validator',
    #                            'error':'analysisspecs_validator',},
    #     subfield_labels = {'keyword': _('Analysis Service'),
    #                        'min': _('Min'),
    #                        'max': _('Max'),
    #                        'error': _('% Error'),
    #                        'hidemin': _('< Min'),
    #                        'hidemax': _('> Max'),
    #                        'rangecomment': _('Range Comment')},
    #     widget = AnalysisSpecificationWidget(
    #         checkbox_bound = 0,
    #         label = _("Specifications"),
    #         description = _("Click on Analysis Categories (against shaded background" \
    #                         "to see Analysis Services in each category. Enter minimum " \
    #                         "and maximum values to indicate a valid results range. " \
    #                         "Any result outside this range will raise an alert. " \
    #                         "The % Error field allows for an % uncertainty to be " \
    #                         "considered when evaluating results against minimum and " \
    #                         "maximum values. A result out of range but still in range " \
    #                         "if the % error is taken into consideration, will raise a " \
    #                         "less severe alert. If the result is below '< Min' " \
    #                         "the result will be shown as '< [min]'. The same " \
    #                         "applies for results above '> Max'"),
    #     ),
    # ),
    # ComputedField('ClientUID',
    #     expression = "context.aq_parent.UID()",
    #     widget = ComputedWidget(
    #         visible = False,
    #     ),
    # ),
)
# schema['description'].widget.visible = True
# schema['title'].required = True

class AnalysisSpec(models.Model, BaseOLiMSModel): #BaseFolder, HistoryAwareMixin
    _name = "olims.analysis_spec"
    _rec_name = "Title"
    # implements(IAnalysisSpec)
    # security = ClassSecurityInfo()
    # schema = schema
    # displayContentsTab = False

    _at_rename_after_creation = True
    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def contextual_title(self):
        parent = self.aq_parent
        if parent == self.bika_setup.bika_analysisspecs:
            return self.title + " ("+translate(_("Lab"))+")"
        else:
            return self.title + " ("+translate(_("Client"))+")"

#    security.declarePublic('getSpecCategories')
    def getSpecCategories(self):
        bsc = getToolByName(self, 'bika_setup_catalog')
        categories = []
        for spec in self.getResultsRange():
            keyword = spec['keyword']
            service = bsc(portal_type="AnalysisService",
                          getKeyword = keyword)
            if service.getCategoryUID() not in categories:
                categories.append(service.getCategoryUID())
        return categories

 #   security.declarePublic('getResultsRangeDict')
    def getResultsRangeDict(self):
        """
            Return a dictionary with the specification fields for each
            service. The keys of the dictionary are the keywords of each
            analysis service. Each service contains a dictionary in which
            each key is the name of the spec field:
            specs['keyword'] = {'min': value,
                                'max': value,
                                'error': value,
                                ... }
        """
        specs = {}
        subfields = self.Schema()['ResultsRange'].subfields
        for spec in self.getResultsRange():
            keyword = spec['keyword']
            specs[keyword] = {}
            for key in subfields:
                if key not in ['uid', 'keyword']:
                    specs[keyword][key] = spec.get(key, '')
        return specs

  #  security.declarePublic('getResultsRangeSorted')
    def getResultsRangeSorted(self):
        """
            Return an array of dictionaries, sorted by AS title:
             [{'category': <title of AS category>
               'service': <title of AS>,
               'id': <ID of AS>
               'uid': <UID of AS>
               'min': <min range spec value>
               'max': <max range spec value>
               'error': <error spec value>
               ...}]
        """
        tool = getToolByName(self, REFERENCE_CATALOG)

        cats = {}
        subfields = self.Schema()['ResultsRange'].subfields
        for spec in self.getResultsRange():
            service = tool.lookupObject(spec['uid'])
            service_title = service.Title()
            category_title = service.getCategoryTitle()
            if not cats.has_key(category_title):
                cats[category_title] = {}
            cat = cats[category_title]
            cat[service_title] = {'category': category_title,
                                  'service': service_title,
                                  'id': service.getId(),
                                  'uid': spec['uid'],
                                  'min': spec['min'],
                                  'max': spec['max'],
                                  'error': spec['error'] }
            for key in subfields:
                if key not in ['uid', 'keyword']:
                    cat[service_title][key] = spec.get(key, '')
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

   # security.declarePublic('getRemainingSampleTypes')
    def getSampleTypes(self):
        """ return all sampletypes """
        sampletypes = []
        bsc = getToolByName(self, 'bika_setup_catalog')
        for st in bsc(portal_type = 'SampleType',
                      sort_on = 'sortable_title'):
            sampletypes.append((st.UID, st.Title))

        return DisplayList(sampletypes)

    def getAnalysisSpecsStr(self, keyword):
        specstr = ''
        specs = self.getResultsRangeDict()
        if keyword in specs.keys():
            specs = specs[keyword]
            smin = specs.get('min', '')
            smax = specs.get('max', '')
            if smin and smax:
                specstr = '%s - %s' % (smin, smax)
            elif smin:
                specstr = '> %s' % specs['min']
            elif smax:
                specstr = '< %s' % specs['max']
        return specstr

    def getClientUID(self):
        return self.aq_parent.UID();

#atapi.registerType(AnalysisSpec, PROJECTNAME)
AnalysisSpec.initialze(schema)

