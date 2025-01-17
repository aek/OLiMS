# ~~~~~~~~~~ Irrelevant code for Odoo ~~~~~~~~~~~
# from dependencies.dependency import ClassSecurityInfo
# from lims import bikaMessageFactory as _
# from lims.utils import t
# from lims.config import PROJECTNAME
# from lims.content.bikaschema import BikaFolderSchema
# from lims.interfaces import IBatch
# from lims.workflow import skip, BatchState, StateFlow, getCurrentState,\
#     CancellationState
# from lims.browser.widgets import DateTimeWidget
# from dependencies.dependency import ATFolder
# from dependencies.dependency import *
# from dependencies.dependency import getToolByName
# from dependencies.dependency import safe_unicode
# from dependencies.dependency import implements
# from lims.permissions import EditBatch
# from dependencies.dependency import indexer
# from dependencies.dependency import HoldingReference
# from dependencies.dependency import RecordsField
# from lims.browser.widgets import RecordsWidget as bikaRecordsWidget
#
# from lims.browser.widgets import ReferenceWidget


from openerp import fields, models
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.date_time_field import DateTimeField
from fields.text_field import TextField
from fields.widget.widget import StringWidget, DateTimeWidget,TextAreaWidget
from lims import bikaMessageFactory as _

BATCHE_STATES = (
    ('open','Open'), ('closed','Closed'),
    )
# ~~~~~~~ To be implemented ~~~~~~~
# class InheritedObjectsUIField(RecordsField):
#
#     """XXX bika.lims.RecordsWidget doesn't cater for multiValued fields
#     InheritedObjectsUI is a RecordsField because we want the RecordsWidget,
#     but the values are stored in ReferenceField 'InheritedObjects'
#     """
#
#     def get(self, instance, **kwargs):
#         # Return the formatted contents of InheritedObjects field.
#         field = instance.Schema()['InheritedObjects']
#         value = field.get(instance)
#         return [{'Title': x.Title(),
#                  'ObjectID': x.id,
#                  'Description': x.Description()} for x in value]
#
#     def getRaw(self, instance, **kwargs):
#         # Return the formatted contents of InheritedObjects field.
#         field = instance.Schema()['InheritedObjects']
#         value = field.get(instance)
#         return [{'Title': x.Title(),
#                  'ObjectID': x.id,
#                  'Description': x.Description()} for x in value]
#
#     def set(self, instance, value, **kwargs):
#         _field = instance.Schema().getField('InheritedObjects')
#         uids = []
#         if value:
#             bc = getToolByName(instance, 'bika_catalog')
#             ids = [x['ObjectID'] for x in value]
#             if ids:
#                 proxies = bc(id=ids)
#                 if proxies:
#                     uids = [x.UID for x in proxies]
#         RecordsField.set(self, instance, value)
#         return _field.set(instance, uids)


#schema = BikaFolderSchema.copy() + Schema((
schema = (StringField(
        'name',
        searchable=True,
        required=True,
        validators=('uniquefieldvalidator',),
        widget=StringWidget(
            visible=False,
            label=_("Batch ID"),
        )
    ),
    TextField('Description',
        widget=TextAreaWidget(
            description = ('Used in item listings and search results.'),
                            )
    ),

    fields.Many2one(string='Client',
                    comodel_name='olims.client',
                    required=False,
     # required=0,
     #    allowed_types=('Client',),
     #    relationship='BatchClient',
     #    widget=ReferenceWidget(
     #        label=_("Client"),
     #        size=30,
     #        visible=True,
     #        base_query={'inactive_state': 'active'},
     #        showOn=True,
     #        colModel=[{'columnName': 'UID', 'hidden': True},
     #                  {'columnName': 'ClientID', 'width': '20', 'label': _('Client ID')},
     #                  {'columnName': 'Title', 'width': '80', 'label': _('Title')}
     #                 ],
     #  ),
    ),

    StringField(
        'ClientBatchID',
        searchable=True,
        required=0,
        widget=StringWidget(
            label=_("Client Batch ID")
        )
    ),
    DateTimeField(
        'BatchDate',
        required=False,
        widget=DateTimeWidget(
            label=_('Date'),
        ),
    ),
          
          fields.Many2many(string='BatchLabels',
                   comodel_name='olims.batch_label',
   #     'BatchLabels',
    #     vocabulary="BatchLabelVocabulary",
    #     accessor="getLabelNames",
    #     widget=MultiSelectionWidget(
    #         label=_("Batch Labels"),
    #         format="checkbox",
    #     )
    ),
# ~~~~~~~  View for Remarks fields does not exist~~~~~~~
#     TextField(
#         'Remarks',
#         searchable=True,
#         default_content_type='text/x-web-intelligent',
#         allowable_content_types=('text/plain', ),
#         default_output_type="text/plain",
#         widget=TextAreaWidget(
#             macro="bika_widgets/remarks",
#             label=_('Remarks'),
#             append_only=True,
#         )
#     ),

    fields.Many2many(string='InheritedObjects',
    comodel_name='olims.inherit_from_batch',
    relation='inheritform_batch',
    required=False,
    ondelete='cascade'
        #     'InheritedObjectsUI',
    #     required=False,
    #     type='InheritedObjects',
    #     subfields=('Title', 'ObjectID', 'Description'),
    #     subfield_sizes = {'Title': 25,
    #                       'ObjectID': 25,
    #                       'Description': 50,
    #                       },
    #     subfield_labels = {'Title': _('Title'),
    #                        'ObjectID': _('Object ID'),
    #                        'Description': _('Description')
    #                        },
    #     widget = bikaRecordsWidget(
    #         label=_("Inherit From"),
    #         description=_(
    #             "Include all analysis requests belonging to the selected objects."),
    #         innerJoin="<br/>",
    #         combogrid_options={
    #             'Title': {
    #                 'colModel': [
    #                     {'columnName': 'Title', 'width': '25',
    #                      'label': _('Title'), 'align': 'left'},
    #                     {'columnName': 'ObjectID', 'width': '25',
    #                      'label': _('Object ID'), 'align': 'left'},
    #                     {'columnName': 'Description', 'width': '50',
    #                      'label': _('Description'), 'align': 'left'},
    #                     {'columnName': 'UID', 'hidden': True},
    #                 ],
    #                 'url': 'getAnalysisContainers',
    #                 'showOn': False,
    #                 'width': '600px'
    #             },
    #             'ObjectID': {
    #                 'colModel': [
    #                     {'columnName': 'Title', 'width': '25',
    #                      'label': _('Title'), 'align': 'left'},
    #                     {'columnName': 'ObjectID', 'width': '25',
    #                      'label': _('Object ID'), 'align': 'left'},
    #                     {'columnName': 'Description', 'width': '50',
    #                      'label': _('Description'), 'align': 'left'},
    #                     {'columnName': 'UID', 'hidden': True},
    #                 ],
    #                 'url': 'getAnalysisContainers',
    #                 'showOn': False,
    #                 'width': '600px'
    #             },
    #         },
    #     ),
    # ),
    ),
    StringField(string='BatchId',compute='_ComputeBatchId'),
    fields.Selection(string='state',selection=BATCHE_STATES,
        default='open', select=True,
        required=True, readonly=True,
        copy=False, track_visibility='always'
        ),

)



# schema['title'].required = False
# schema['title'].widget.visible = True
# schema['title'].widget.description = _("If no Title value is entered, the Batch ID will be used.")
# schema['description'].required = False
# schema['description'].widget.visible = True
#
# schema.moveField('ClientBatchID', before='description')
# schema.moveField('BatchID', before='description')
# schema.moveField('title', before='description')
# schema.moveField('Client', after='title')


class Batch(models.Model, BaseOLiMSModel): #ATFolder
    _name='olims.batch'

    # implements(IBatch)
    # security = ClassSecurityInfo()
    # displayContentsTab = False
    # schema = schema

    def _ComputeBatchId(self):
        for record in self:
            batchidstring = 'B-0' + str(record.id)
            record.BatchId = batchidstring

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        from lims.idserver import renameAfterCreation
        renameAfterCreation(self)

    def Title(self):
        """ Return the Batch ID if title is not defined """
        titlefield = self.Schema().getField('title')
        if titlefield.widget.visible:
            return safe_unicode(self.title).encode('utf-8')
        else:
            return safe_unicode(self.id).encode('utf-8')

    def _getCatalogTool(self):
        from lims.catalog import getCatalog
        return getCatalog(self)

    def getClient(self):
        """ Retrieves the Client for which the current Batch is attached to
            Tries to retrieve the Client from the Schema property, but if not
            found, searches for linked ARs and retrieve the Client from the
            first one. If the Batch has no client, returns None.
        """
        client = self.Schema().getField('Client').get(self)
        if client:
            return client
        return client

    def getClientTitle(self):
        client = self.getClient()
        if client:
            return client.Title()
        return ""

    def getContactTitle(self):
        return ""

    def getProfilesTitle(self):
        return ""

    def getAnalysisCategory(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getCategoryTitle()
            if val not in value:
                value.append(val)
        return value

    def getAnalysisService(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getServiceTitle()
            if val not in value:
                value.append(val)
        return value

    def getAnalysts(self):
        analyses = []
        for ar in self.getAnalysisRequests():
            analyses += list(ar.getAnalyses(full_objects=True))
        value = []
        for analysis in analyses:
            val = analysis.getAnalyst()
            if val not in value:
                value.append(val)
        return value

    #security.declarePublic('getBatchID')

    def getBatchID(self):
        return self.getId()

    def BatchLabelVocabulary(self):
        """ return all batch labels """
        bsc = getToolByName(self, 'bika_setup_catalog')
        ret = []
        for p in bsc(portal_type='BatchLabel',
                     inactive_state='active',
                     sort_on='sortable_title'):
            ret.append((p.UID, p.Title))
        return DisplayList(ret)

    def getAnalysisRequests(self):
        """ Return all the Analysis Requests linked to the Batch
        """
        return self.getBackReferences("AnalysisRequestBatch")

    def isOpen(self):
        """ Returns true if the Batch is in 'open' state
        """
        revstatus = getCurrentState(self, StateFlow.review)
        canstatus = getCurrentState(self, StateFlow.cancellation)
        return revstatus == BatchState.open \
            and canstatus == CancellationState.active

    def getLabelNames(self):
        uc = getToolByName(self, 'uid_catalog')
        uids = [uid for uid in self.Schema().getField('BatchLabels').get(self)]
        labels = [label.getObject().title for label in uc(UID=uids)]
        return labels

    def workflow_guard_open(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'closed' or 'cancelled'
            The open transition is already controlled by 'Bika: Reopen Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific-needs.
        """
        return self.write(cr, uid, ids, {'state': 'open'}, context=context)
        # revstatus = getCurrentState(self, StateFlow.review)
        # canstatus = getCurrentState(self, StateFlow.cancellation)
        # return revstatus == BatchState.closed \
        #     and canstatus == CancellationState.active

    def workflow_guard_close(self, cr, uid, ids, context=None):
        """ Permitted if current review_state is 'open'.
            The close transition is already controlled by 'Bika: Close Batch'
            permission, but left here for security reasons and also for the
            capability of being expanded/overrided by child products or
            instance-specific needs.
        """
        return self.write(cr, uid, ids, {'state': 'closed'}, context=context)
        # revstatus = getCurrentState(self, StateFlow.review)
        # canstatus = getCurrentState(self, StateFlow.cancellation)
        # return revstatus == BatchState.open \
        #     and canstatus == CancellationState.active


#registerType(Batch, PROJECTNAME)
Batch.initialze(schema)

# @indexer(IBatch)
# def BatchDate(instance):
#     return instance.Schema().getField('BatchDate').get(instance)
