# -*- coding: utf-8 -*-
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.app.textfield import RichText
from plone.formwidget.contenttree import ObjPathSourceBinder
from z3c.relationfield.schema import RelationChoice

from eea.glossary import _
from eea.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from constants import SUBJECTS


subjects = SimpleVocabulary([SimpleTerm(value=value, title=title)
                             for value, title in SUBJECTS])


class IGlossaryLayer(Interface):

    """A layer specific for this add-on product."""


class IGlossarySettings(Interface):

    """Schema for the control panel form."""

    enable_tooltip = schema.Bool(
        title=_(u'Enable tooltip?'),
        description=_(u'Enable tooltip.'),
        default=True,
    )

    enabled_content_types = schema.List(
        title=_(u'Enabled Content Types'),
        description=_(u'Only objects of these content types will display '
                      'glossary terms.'),
        required=False,
        default=DEFAULT_ENABLED_CONTENT_TYPES,
        # we are going to list only the main content types in the widget
        value_type=schema.Choice(
            vocabulary=u'eea.glossary.PortalTypes'),
    )


class IGlossary(Interface):

    """A Glossary is a container for Terms."""

    text = RichText(
        title=_(u'Body text'),
        description=_(u''),
        required=False,
    )


class ITerm(Interface):

    """A Term."""

    source = schema.TextLine(
        title=_(u"Source"),
        required=False,
    )

    context = schema.TextLine(
        title=_(u"Context"),
        required=False,
    )

    comment = schema.Text(
        title=_(u'Comment'),
        required=False,
    )

    definition_source_publication = schema.TextLine(
        title=_(u"Definition source publication"),
        required=False,
    )

    publication_year = schema.Int(
        title=_(u"Publication year"),
        required=False,
    )

    definition_source_url = schema.TextLine(
        title=_(u"Definition source URL"),
        required=False,
    )

    organisation = schema.TextLine(
        title=_(u"Organisation"),
        required=False,
    )

    organisation_fullname = schema.TextLine(
        title=_(u"Organisation full name"),
        required=False,
    )

    subjects = schema.Set(
        title=_(u"Subjects"),
        value_type=schema.Choice(source=subjects),
        required=False,
    )

    long_definition = schema.Text(
        title=_(u'Long definition'),
        required=False,
    )


class ISynonym(Interface):

    """A Synonym."""

    term = RelationChoice(
        title=_(u"Term"),
        source=ObjPathSourceBinder(object_provides=ITerm.__identifier__),
        required=True,
    )
