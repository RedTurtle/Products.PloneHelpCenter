try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
from AccessControl import ClassSecurityInfo
from Products.PloneHelpCenter.config import phcMessageFactory as _
from Products.PloneHelpCenter.config import PROJECTNAME, IMAGE_SIZES
from schemata import HelpCenterBaseSchema, GenericHelpCenterItemSchema
from PHCContent import PHCContent

InstructionalVideoSchema = HelpCenterBaseSchema + Schema((
    TextField(
        'description',
        default='',
        required=1,
        searchable=1,
        accessor="Description",
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        storage=MetadataStorage(),
        widget=TextAreaWidget(
                 description=_("phc_help_detailed_video",
                               default=u"Brief explanation of the video's content."),
                 label=_("phc_label_detailed_video",
                         default=u"Summary"),
              ),
        ),

    FileField(
        'video_file',
        required=1,
        primary=1,
        widget=FileWidget(
            description=_("phc_help_videofile_description",
                          default=u"Click 'Browse' to upload a Flash .swf file."),
            label=_("phc_label_videofile_description",
                    default=u"Flash File (.swf)"),
            ),
        ),

    ImageField(
        'screenshot',
        required=0,
        sizes=IMAGE_SIZES,
        widget=ImageWidget(
            label=_('phc_label_video_screenshot',
                    default=u'Screenshot'),
            description=_('phc_help_video_screenshot',
                          default=u"""Add a screenshot by clicking the "Browse" button.
                          Add a screenshot that highlights the content of the instructional video."""),
            ),
        ),

    StringField(
        'duration',
        required=0,
        widget=StringWidget(
            description=_('phc_help_video_duration',
                          default=u'Length (in minutes) of the video.'),
            label=_('phc_label_video_duration',
                    default=u'Duration'),
            ),
        ),

    IntegerField(
        'width',
        required=0,
        default='800',
        validators=('isInt',),
        widget=IntegerWidget(
            description=_('phc_help_video_width',
                          default=u'Width of the video.'),
            label=_('phc_label_video_width',
                    default=u'Width'),
            ),
        ),

    IntegerField(
        'height',
        required=0,
        default='600',
        validators=('isInt',),
        widget=IntegerWidget(
            description=_('phc_help_video_height',
                          default=u'Height of the video.'),
            label=_('phc_label_video_height',
                    default='Height'),
            ),
        ),
    ),

    marshall=PrimaryFieldMarshaller(),

    ) + GenericHelpCenterItemSchema

# For some reason, we need to jump through these hoops to get the fields in the
# the right order
InstructionalVideoSchema.moveField('subject', pos='bottom')
InstructionalVideoSchema.moveField('relatedItems', pos='bottom')


class HelpCenterInstructionalVideo(PHCContent, BaseContent):
    """This is an Instructional Video content type, to which you can attach
    movies and other relevant files.
    """

    content_icon = 'movie_icon.gif'

    schema = InstructionalVideoSchema
    archetype_name = 'Video'
    meta_type = 'HelpCenterInstructionalVideo'
    global_allow = 0
    # allow_discussion = IS_DISCUSSABLE

    typeDescription = 'An Instructional Video can be used to upload Flash instructional videos.'
    typeDescMsgId = 'description_edit_instructionalvideo'

    # aliases = PHCContent.aliases.copy()
    # aliases.update({'(Default)' : 'ivideo_view',
    #                 'view'      : 'ivideo_view'})

    security = ClassSecurityInfo()

registerType(HelpCenterInstructionalVideo, PROJECTNAME)
