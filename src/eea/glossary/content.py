# -*- coding: utf-8 -*-
from eea.glossary.interfaces import IGlossary
from eea.glossary.interfaces import ITerm
from eea.glossary.interfaces import ISynonym
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from zope.interface import implementer


@implementer(IGlossary)
class Glossary(Container):

    """A Glossary is a container for Terms and Synonyms."""


@implementer(ITerm)
class Term(Item):

    """A Term."""


@implementer(ISynonym)
class Synonym(Item):

    """A Synonym."""
