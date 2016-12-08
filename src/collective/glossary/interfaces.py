# -*- coding: utf-8 -*-
from collective.glossary import _
from collective.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
from plone.app.textfield import RichText
from zope import schema
from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


subjects = SimpleVocabulary([
    SimpleTerm(value=u'ADMLEG', title=_(u'Administration and Legislation')),
    SimpleTerm(value=u'AGRARE', title=_(u'Agriculture and Rural Areas')),
    SimpleTerm(value=u'AIRCHA', title=_(u'Air and Climate Change')),
    SimpleTerm(value=u'CHEHEA', title=_(u'CHEMICALS AND HEALTH')),
    SimpleTerm(value=u'DATINF', title=_(u'DATA MANAGEMENT AND INFORMATION')),
    SimpleTerm(value=u'ECOREP',
               title=_(u'ECONOMICS AND CORPORATE REPORTING')),
    SimpleTerm(value=u'EIO', title=_(u'EIONET')),
    SimpleTerm(value=u'ENE', title=_(u'ENERGY')),
    SimpleTerm(value=u'ENVIND', title=_(u'ENVIRONMENTAL INDICATORS')),
    SimpleTerm(value=u'ENVINS', title=_(u'ENVIRONMENTAL INSTRUMENTS')),
    SimpleTerm(value=u'GEN', title=_(u'GENERAL')),
    SimpleTerm(value=u'IMPASS', title=_(u'IMPACT ASSESSMENT')),
    SimpleTerm(value=u'INTASS',
               title=_(u'INTEGRATED TOOLS AND METHODOLOGIES FOR ASSESSMENT')),
    SimpleTerm(value=u'LANUSE', title=_(u'LAND COVER AND LAND USE')),
    SimpleTerm(value=u'MARENV', title=_(u'MARINE AND COASTAL ENVIRONMENT')),
    SimpleTerm(value=u'NATBIO', title=_(u'NATURE AND BIODIVERSITY')),
    SimpleTerm(value=u'NATHAZ',
               title=_(u'NATURAL AND TECHNOLOGICAL HAZARDS')),
    SimpleTerm(value=u'NOI', title=_(u'NOISE')),
    SimpleTerm(value=u'SCEANA',
               title=_(u'SCENARIOS AND PROSPECTIVE ANALYSIS')),
    SimpleTerm(value=u'SOI', title=_(u'SOIL')),
    SimpleTerm(value=u'TOU', title=_(u'TOURISM')),
    SimpleTerm(value=u'TRA', title=_(u'TRANSPORT')),
    SimpleTerm(value=u'URBENV', title=_(u'URBAN ENVIRONMENT')),
    SimpleTerm(value=u'WAS', title=_(u'WASTE')),
    SimpleTerm(value=u'WAT', title=_(u'WATER')),
])


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
            vocabulary=u'collective.glossary.PortalTypes'),
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

    disabled = schema.Bool(
        title=_(u"Disabled"),
        required=False,
        default=False,
    )

    long_definition = schema.Text(
        title=_(u'Long definition'),
        required=False,
    )

    qa_needed = schema.Bool(
        title=_(u"QA needed"),
        required=False,
        default=False,
     )
