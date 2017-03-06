# -*- coding: utf-8 -*-
''' test views module  '''
import unittest
from z3c.relationfield import RelationValue
from zope.intid.interfaces import IIntIds
from eea.glossary.interfaces import IGlossarySettings
from eea.glossary.testing import INTEGRATION_TESTING
from plone import api
from zope.publisher.browser import TestRequest
from zope.component import getUtility


class BaseViewTestCase(unittest.TestCase):
    ''' Base View test case '''

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        intids = getUtility(IIntIds)

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(
                self.portal, 'Glossary', 'g1',
                title='Glossary',
                description='Glossary Description'
            )
            self.t1 = api.content.create(
                self.g1, 'Term', 't1',
                title='First Term',
                description='First Term Description',
                comment='First Term Comment',
                context='First Term Context',
                long_definition='First Term Long Definition',
                organisation_fullname='First Term Organisation Full Name',
                organisation='First Term Organisation',
                publication_year=2000,
                source='First Term Source',
                subjects=['NATBIO'],
                definition_source_url='First Term Definition Source URL',
                definition_source_publication=(
                    'First Term Definition Source Publication'),
            )
            self.t2 = api.content.create(
                self.g1, 'Term', 't2',
                title='Second Term',
                description='Second Term Description',
                comment='Second Term Comment',
                context='Second Term Context',
                long_definition='Second Term Long Definition',
                organisation_fullname='Second Term Organisation Full Name',
                organisation='Second Term Organisation',
                publication_year=2001,
                source='Second Term Source',
                subjects=['NATBIO'],
                definition_source_url='Second Term Definition Source',
                definition_source_publication=(
                    'Second Term Definition Source Publication')
            )
            self.s1 = api.content.create(
                self.g1, 'Synonym', 's1',
                title='First Synonym',
                description='First Synonym Description',
                term=RelationValue(intids.getId(self.t1))
            )
            self.s2 = api.content.create(
                self.g1, 'Synonym', 's2',
                title='Second Synonym',
                description='Second Synonym Description',
                term=RelationValue(intids.getId(self.t1))
            )
            self.d1 = api.content.create(
                self.portal, 'Document', 'd1',
                title='Document',
                description='Document Description'
            )


class TermViewTestCase(BaseViewTestCase):
    ''' Term View Test Case '''

    def setUp(self):
        super(TermViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.t1, self.request)

    def test_get_entry(self):
        ''' test get entry '''
        self.assertEqual(
            self.view.get_entry(),
            {'description': u'First Term Description',
             'comment': 'First Term Comment',
             'context': 'First Term Context',
             'long_definition': 'First Term Long Definition',
             'organisation_fullname': 'First Term Organisation Full Name',
             'organisation': 'First Term Organisation',
             'publication_year': 2000,
             'source': 'First Term Source',
             'subjects': ['NATBIO'],
             'definition_source_url': 'First Term Definition Source URL',
             'definition_source_publication':
                'First Term Definition Source Publication',
             'title': u'First Term'}
        )


class SynonymViewTestCase(BaseViewTestCase):
    ''' Synonym view test case '''

    def setUp(self):
        super(SynonymViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.s1, self.request)

    def test_get_entry(self):
        ''' test get entry '''
        entry = self.view.get_entry()
        term = entry.pop('term')
        self.assertEqual(
            entry,
            {'description': 'First Synonym Description',
             'title': 'First Synonym'}
        )
        self.assertTrue(isinstance(term, RelationValue))


class GlossaryViewTestCase(BaseViewTestCase):
    ''' Glossary view test case '''

    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.g1, self.request)

    def test_get_entries(self):
        ''' test get entries '''
        self.assertEqual(
            self.view.get_entries(),
            {
                'F': [
                    {'description': u'First Synonym Description',
                     'title': u'First Synonym'},
                    {'description': u'First Term Description',
                     'title': u'First Term'}
                ],
                'S': [
                    {'description': u'Second Synonym Description',
                     'title': u'Second Synonym'},
                    {'description': u'Second Term Description',
                     'title': u'Second Term'}
                ]
            }
        )

    def test_letters(self):
        ''' test letters '''
        self.assertEqual(self.view.letters(), [u'F', u'S'])

        with api.env.adopt_roles(['Manager']):
            self.ta1 = api.content.create(
                self.g1, 'Term', 'ta1',
                title='American',
                description='American Term Description'
            )
            self.ta2 = api.content.create(
                self.g1, 'Term', 'ta2',
                title='Ásia',
                description='Ásia Term Description'
            )
            self.sa1 = api.content.create(
                self.g1, 'Synonym', 'sa1',
                title='American',
                description='American Synonym Description'
            )
            self.sa2 = api.content.create(
                self.g1, 'Synonym', 'sa2',
                title='Ásia',
                description='Ásia Synonym Description'
            )
        self.assertEqual(self.view.letters(), [u'A', u'F', u'S'])

    def test_terms(self):
        ''' test terms '''
        self.assertEqual(
            self.view.terms('F'),
            [{'description': 'First Synonym Description',
              'title': 'First Synonym'},
             {'description': 'First Term Description',
              'title': 'First Term'}]
        )
        self.assertEqual(
            self.view.terms('S'),
            [{'description': 'Second Synonym Description',
              'title': 'Second Synonym'},
             {'description': 'Second Term Description',
              'title': 'Second Term'}]
        )


class GlossaryStateViewTestCase(BaseViewTestCase):
    ''' Glossary State view test case '''

    def setUp(self):
        super(GlossaryStateViewTestCase, self).setUp()
        self.view = api.content.get_view(u'glossary_state',
                                         self.portal, self.request)

    def test_tooltip_is_enabled(self):
        ''' test tooltip is enabled '''
        api.portal.set_registry_record(
            IGlossarySettings.__identifier__ + '.enable_tooltip',
            True
        )
        self.assertTrue(self.view.tooltip_is_enabled)

        api.portal.set_registry_record(
            IGlossarySettings.__identifier__ + '.enable_tooltip',
            False
        )
        self.assertFalse(self.view.tooltip_is_enabled)

    def test_content_type_is_enabled(self):
        ''' test content type is enabled '''
        self.assertFalse(self.view.content_type_is_enabled)

        self.view.context = self.d1
        self.assertTrue(self.view.content_type_is_enabled)

        self.view.context = self.g1
        self.assertFalse(self.view.content_type_is_enabled)

    def test_is_view_action(self):
        ''' test is view action '''
        self.assertTrue(self.view.is_view_action)

        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost',
            'PATH_INFO': '/folder_contents'
        })
        self.view.request.base = 'http://nohost/plone'
        self.assertFalse(self.view.is_view_action)

        self.view.context = self.g1
        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost/plone/g1',
            'PATH_INFO': '/g1'
        })
        self.view.request.base = 'http://nohost/plone'
        self.assertTrue(self.view.is_view_action)

        self.view.request = TestRequest(environ={
            'SERVER_URL': 'http://nohost/plone/g1',
            'PATH_INFO': '/g1/edit'
        })
        self.view.request.base = 'http://nohost/plone'
        self.assertFalse(self.view.is_view_action)


class JsonViewTestCase(BaseViewTestCase):
    ''' Json view test case '''

    def setUp(self):
        super(JsonViewTestCase, self).setUp()
        self.view = api.content.get_view(
            u'glossary',
            self.portal,
            self.request
        )

    def test_get_json_entries(self):
        ''' test get json entries '''
        self.assertEqual(
            self.view.get_json_entries(),
            [{'description': 'First Term Description', 'term': 'First Term'},
             {'description': 'Second Term Description', 'term': 'Second Term'},
             {'description': 'First Synonym Description',
              'synonym': 'First Synonym'},
             {'description': 'Second Synonym Description',
              'synonym': 'Second Synonym'}]
        )

    def test__call__(self):
        ''' test call '''
        import json

        self.view()
        result = self.view.request.response.getBody()
        self.assertEqual(
            json.loads(result),
            [{u'description': u'First Term Description',
              u'term': u'First Term'},
             {u'description': u'Second Term Description',
              u'term': u'Second Term'},
             {u'description': u'First Synonym Description',
              u'synonym': u'First Synonym'},
             {u'description': u'Second Synonym Description',
              u'synonym': u'Second Synonym'}]
        )
