from AccessControl import ClassSecurityInfo

try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
from Products.PloneHelpCenter.config import phcMessageFactory as _
from Products.PloneHelpCenter.config import PROJECTNAME
from HowTo import HowToSchema, HelpCenterHowTo

ErrorReferenceSchema = HowToSchema.copy()
# del ErrorReferenceSchema['versions']
# del ErrorReferenceSchema['sections']
# del ErrorReferenceSchema['audiences']
# del ErrorReferenceSchema['startHere']
ErrorReferenceSchema['text'].widget.description = _('phc_help_body_ErrorReference',
                                                    default=u'Explanation of the error.')


class HelpCenterErrorReference(HelpCenterHowTo):
    """An Error Reference can be used to explain a particular error which may
    arise.
    """

    content_icon = 'errorref_icon.gif'

    schema = ErrorReferenceSchema
    archetype_name = 'Error Reference'
    meta_type = 'HelpCenterErrorReference'

    typeDescription = 'An Error Reference can be used to explain a particular error which may arise.'
    typeDescMsgId = 'description_edit_errorreference'

    security = ClassSecurityInfo()

registerType(HelpCenterErrorReference, PROJECTNAME)
