# -*- coding: utf-8 -*-
""" Vocabulary module """
from plone.app.vocabularies.types import ReallyUserFriendlyTypesVocabulary
from zope.schema.vocabulary import SimpleVocabulary


class PortalTypesVocabulary(ReallyUserFriendlyTypesVocabulary):
    """Inherit from plone.app.vocabularies.ReallyUserFriendlyTypes; and
    filter the results. We don't want Glossary, Term or Synonym to be listed.
    """

    def __call__(self, context):
        items = super(PortalTypesVocabulary, self).__call__(context)
        items = [i for i in items if i.token not in ('Glossary',
                                                     'Term',
                                                     'Synonym')]
        return SimpleVocabulary(items)

PortalTypesVocabularyFactory = PortalTypesVocabulary()
