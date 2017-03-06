# -*- coding: utf-8 -*-
''' test synonyms '''

import unittest

from eea.glossary.interfaces import ISynonym
from eea.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility


class GlossaryTypeTestCase(unittest.TestCase):
    ''' Glossary test case '''

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(self.portal, 'Glossary', 'g1')

        self.s1 = api.content.create(self.g1, 'Synonym', 's1')

    def test_adding(self):
        ''' test adding Synonym '''
        self.assertTrue(ISynonym.providedBy(self.s1))

    def test_adding_outside_glossary(self):
        ''' test adding outside of glossary '''
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.portal, 'Synonym', 'test')

    def test_fti(self):
        ''' test fti '''
        fti = queryUtility(IDexterityFTI, name='Synonym')
        self.assertIsNotNone(fti)

    def test_schema(self):
        ''' test schema '''
        fti = queryUtility(IDexterityFTI, name='Synonym')
        schema = fti.lookupSchema()
        self.assertEqual(ISynonym, schema)

    def test_factory(self):
        ''' test factory '''
        fti = queryUtility(IDexterityFTI, name='Synonym')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ISynonym.providedBy(new_object))
