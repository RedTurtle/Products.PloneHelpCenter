try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *
from Products import ATContentTypes
from Products.ATContentTypes.content.document import ATDocumentBase
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from Products.PloneHelpCenter.config import phcMessageFactory as _
from Products.PloneHelpCenter.config import PROJECTNAME
from schemata import HelpCenterItemSchemaNarrow
from PHCContent import PHCContentMixin

FAQSchema = ATContentTypes.content.document.ATDocumentSchema.copy() + HelpCenterItemSchemaNarrow
FAQSchema['description'].widget = \
    TextAreaWidget(
        description=_("help_detailed_question",
                      default=u'More details on the question, if not evident from the title.'),
        label=_("label_detailed_question",
                default=u"Detailed Question"),
        rows=5,
        )
FAQSchema['text'].widget.label = "Answer"
FAQSchema['text'].widget.label_msgid = "label_answer"
FAQSchema['text'].widget.i18n_domain = "plonehelpcenter"

finalizeATCTSchema(FAQSchema, folderish=False, moveDiscussion=False)


class HelpCenterFAQ(ATDocumentBase, PHCContentMixin):
    """A Frequently Asked Question defines a common question with an answer -
    this is a place to document answers to common questions, not ask them.
    """

    content_icon = 'faq_icon.gif'

    schema = FAQSchema
    archetype_name = 'FAQ'
    meta_type = 'HelpCenterFAQ'

    typeDescription = 'A Frequently Asked Question defines a common question with an answer - this is a place to document answers to common questions, not ask them.'
    typeDescMsgId = 'description_edit_faq'


registerType(HelpCenterFAQ, PROJECTNAME)
