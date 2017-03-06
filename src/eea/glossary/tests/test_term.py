# -*- coding: utf-8 -*-
''' test term module '''

import unittest

from eea.glossary.interfaces import ITerm
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

        self.t1 = api.content.create(self.g1, 'Term', 't1')

    def test_adding(self):
        ''' test adding '''
        self.assertTrue(ITerm.providedBy(self.t1))

    def test_adding_outside_glossary(self):
        ''' test adding outside of glossary '''
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.portal, 'Term', 'test')

    def test_fti(self):
        ''' test fti '''
        fti = queryUtility(IDexterityFTI, name='Term')
        self.assertIsNotNone(fti)

    def test_schema(self):
        ''' test schema '''
        fti = queryUtility(IDexterityFTI, name='Term')
        schema = fti.lookupSchema()
        self.assertEqual(ITerm, schema)

    def test_factory(self):
        ''' test factory '''
        fti = queryUtility(IDexterityFTI, name='Term')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(ITerm.providedBy(new_object))
