try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
try:
    import Products.CMFCore.permissions as CMFCorePermissions
except ImportError:
    from Products.CMFCore import CMFCorePermissions
from Products.PloneHelpCenter.config import phcMessageFactory as _
from Products.PloneHelpCenter.config import REFERENCEABLE_TYPES, GLOBAL_RIGHTS

from Products import ATContentTypes as atct

try:
    from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
    PHCReferenceWidget = ReferenceBrowserWidget
except ImportError:
    PHCReferenceWidget = ReferenceWidget

try:
    from Products.AddRemoveWidget import AddRemoveWidget
    PHCKeywordWidget = AddRemoveWidget
except ImportError:
    PHCKeywordWidget = KeywordWidget


###########################################
# Common components to Help Types schemas #
###########################################

HelpCenterItemSchema = Schema((

    LinesField(
        'versions',
        languageIndependent=1,
        index='KeywordIndex',
        vocabulary='getVersionsVocab',
        condition='object/getVersionsVocab',
        multiValued=1,
        required=0,
        widget=MultiSelectionWidget(
                label=_('phc_label_versions',
                        default=u"Versions"),
                condition='object/getVersionsVocab',
                description=_("phc_versions",
                              default=u"""'Versions of product that apply to this item
                                       (leave blank if not version-specific)."""),
                ),
        ),

    LinesField(
        'sections',
        multiValued=1,
        required=0,
        vocabulary='getSectionsVocab',
        condition='object/getSectionsVocab',
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label=_("phc_label_sections",
                        default=u'Sections'),
                condition='object/getSectionsVocab',
                description=_("phc_sections",
                              default=u'Section(s) that this item should appear in.'),
                ),
        ),

    LinesField(
        'audiences',
        multiValued=1,
        required=0,
        vocabulary='getAudiencesVocab',
        condition="object/getAudiencesVocab",
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label=_("phc_label_audiences",
                        default=u'Audiences'),
                description=_("phc_audiences",
                              default=u'Audience(s) this item is targetted at.'),
                condition="object/getAudiencesVocab",
                ),
        ),

    LinesField(
        'contributors',
        accessor="Contributors",
        languageIndependent=1,
        widget=LinesWidget(
                label=_("label_contributors",
                        default=u'Contributors'),
                description=_("help_contributors",
                              default=u"Enter additional names (no need to include the current owner) for those who have contributed to this entry, one per line."),
                ),
        ),

    LinesField(
        'subject',
        accessor='Subject',
        searchable=1,
        vocabulary='getSubjectVocab',
        enforceVocabulary=0,
        isMetadata=1,
        widget=PHCKeywordWidget(
                label=_("phc_label_related",
                        default=u'Related keywords'),
        ),
    ),

    BooleanField(
        'startHere',
        index='FieldIndex:schema',
        permission=CMFCorePermissions.ReviewPortalContent,
        widget=BooleanWidget(
                label=_("phc_label_starthere",
                        default=u'Start Here'),
                description=_("phc_starthere",
                              default=u"Marks this as a good starting point for its section. Only key documents should have this property."),
        ),
    ),

    ReferenceField(
        'relatedItems',
        relationship='PloneHelpCenter',
        allowed_types=REFERENCEABLE_TYPES,
        required=0,
        multiValued=1,
        languageIndependent=1,
        widget=PHCReferenceWidget(
                label=_("phc_label_reference",
                        default=u"Referenced Items"),
                description=_("phc_reference",
                              default=u"Set one or more references to HelpCenter items."),
                ),
    ),

))

# a version that doesn't duplicate any
# extensibleMetadata fields.
HelpCenterItemSchemaNarrow = Schema((
    LinesField(
        'versions',
        languageIndependent=1,
        index='KeywordIndex',
        vocabulary='getVersionsVocab',
        condition='object/getVersionsVocab',
        multiValued=1,
        required=0,
        widget=MultiSelectionWidget(
                label=_('phc_label_versions',
                        default=u"Versions"),
                condition='object/getVersionsVocab',
                description=_("phc_versions",
                              default=u"""Versions of product that apply to this item
                              (leave blank if not version-specific)."""),
                ),
        ),

    LinesField(
        'sections',
        multiValued=1,
        required=0,
        vocabulary='getSectionsVocab',
        condition='object/getSectionsVocab',
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
                label=_("phc_label_sections",
                        default=u'Sections'),
                condition='object/getSectionsVocab',
                description=_("phc_sections",
                              default=u'Section(s) that this item should appear in.'),
                ),
        ),

    LinesField(
        'audiences',
        multiValued=1,
        required=0,
        vocabulary='getAudiencesVocab',
        condition="object/getAudiencesVocab",
        index='KeywordIndex',
        widget=MultiSelectionWidget(
                label=_("phc_label_audiences",
                        default=u'Audiences'),
                description=_("phc_audiences",
                              default=u'Audience(s) this item is targetted at.'),
                condition="object/getAudiencesVocab",
                ),
        ),

    BooleanField(
        'startHere',
        index='FieldIndex',
        permission=CMFCorePermissions.ReviewPortalContent,
        widget=BooleanWidget(
                label=_("phc_label_starthere",
                        default=u'Start Here'),
                description=_("phc_starthere",
                              default=u"Marks this as a good starting point for its section. Only key documents should have this property."),

        ),
    ),

))

GenericHelpCenterItemSchema = HelpCenterItemSchema.copy()
del GenericHelpCenterItemSchema['audiences']

# what sections should there be? (for enclosing folders, not indiv items!)
HelpCenterContainerSchema = Schema((

    LinesField(
        'sectionsVocab',
        accessor='getSectionsVocab',
        edit_accessor='getRawSectionsVocab',
        mutator='setSectionsVocab',
        widget=LinesWidget(
            label=_("phc_label_sections-vocab",
                    default=u"Sections"),
            description=_("phc_sections_vocab",
                          default="""One section on each line. Used for grouping items.
                          If you leave this blank, the help center's
                          sections will be used. If both are blank,
                          sections will not be used."""),
            rows=6,
            )
        ),
    ))

# non folderish Help Center Base schemata
HelpCenterBaseSchema = BaseSchema.copy()

# folderish Help Center Base schemata
HelpCenterBaseSchemaFolderish = atct.content.folder.ATFolderSchema.copy()


# Remove "contributors" from metadata, so that we can add it later
if GLOBAL_RIGHTS:
    del HelpCenterBaseSchema['contributors']
    del HelpCenterBaseSchema['rights']
