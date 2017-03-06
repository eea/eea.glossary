# -*- coding: utf-8 -*-
''' test glossary module '''

import unittest

from eea.glossary.interfaces import IGlossary
from eea.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility


class GlossaryTypeTestCase(unittest.TestCase):
    ''' Glossary type test case '''

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(self.portal, 'Glossary', 'g1')

    def test_adding(self):
        ''' test add '''
        self.assertTrue(IGlossary.providedBy(self.g1))

    def test_fti(self):
        ''' test fti '''
        fti = queryUtility(IDexterityFTI, name='Glossary')
        self.assertIsNotNone(fti)

    def test_schema(self):
        ''' test schema '''
        fti = queryUtility(IDexterityFTI, name='Glossary')
        schema = fti.lookupSchema()
        self.assertEqual(IGlossary, schema)

    def test_factory(self):
        ''' test factory '''
        fti = queryUtility(IDexterityFTI, name='Glossary')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IGlossary.providedBy(new_object))

    def test_is_selectable_as_folder_default_view(self):
        ''' test selectable '''
        self.portal.setDefaultPage('g1')
        self.assertEqual(self.portal.default_page, 'g1')

    def test_not_allowed_content_types(self):
        ''' test content type not allowed '''
        from plone.api.exc import InvalidParameterError
        with self.assertRaises(InvalidParameterError):
            api.content.create(self.g1, 'Document', 'test')
