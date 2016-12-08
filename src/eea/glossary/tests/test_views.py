# -*- coding: utf-8 -*-
from eea.glossary.interfaces import IGlossarySettings
from eea.glossary.testing import INTEGRATION_TESTING
from plone import api
from zope.publisher.browser import TestRequest

import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.g1 = api.content.create(
                self.portal, 'Glossary', 'g1',
                title='Glossary',
                description='Glossary Description'
            )
            self.t1 = api.content.create(
                self.g1, 'Term', 't1',
                title='First Term',
                description='First Term Description'
            )
            self.t2 = api.content.create(
                self.g1, 'Term', 't2',
                title='Second Term',
                description='Second Term Description'
            )
            self.s1 = api.content.create(
                self.g1, 'Synonym', 's1',
                title='First Synonym',
                description='First Synonym Description'
            )
            self.t2 = api.content.create(
                self.g1, 'Synonym', 's2',
                title='Second Synonym',
                description='Second Synonym Description'
            )
            self.d1 = api.content.create(
                self.portal, 'Document', 'd1',
                title='Document',
                description='Document Description'
            )


class TermViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(TermViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.t1, self.request)

    def test_get_entry(self):
        self.assertEqual(
            self.view.get_entry(),
            {'description': 'First Term Description',
             'title': 'First Term'}
        )


class SynonymViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(SynonymViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.s1, self.request)

    def test_get_entry(self):
        self.assertEqual(
            self.view.get_entry(),
            {'description': 'First Synonym Description',
             'title': 'First Synonym'}
        )


class GlossaryViewTestCase(BaseViewTestCase):

    def setUp(self):
        super(GlossaryViewTestCase, self).setUp()
        self.view = api.content.get_view(u'view', self.g1, self.request)

    def test_get_entries(self):
        self.assertEqual(
            self.view.get_entries(),
            {
                'F': [
                    {'description': 'First Synonym Description',
                     'title': 'First Term'},
                    {'description': 'First Term Description',
                     'title': 'First Term'}
                ],
                'S': [
                    {'description': 'Second Term Description',
                     'title': 'Second Term'},
                    {'description': 'Second Synonym Description',
                     'title': 'Second Term'}
                ]
            }
        )

    def test_letters(self):
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

    def setUp(self):
        super(GlossaryStateViewTestCase, self).setUp()
        self.view = api.content.get_view(u'glossary_state',
                                         self.portal, self.request)

    def test_tooltip_is_enabled(self):
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
        self.assertFalse(self.view.content_type_is_enabled)

        self.view.context = self.d1
        self.assertTrue(self.view.content_type_is_enabled)

        self.view.context = self.g1
        self.assertFalse(self.view.content_type_is_enabled)

    def test_is_view_action(self):
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

    def setUp(self):
        super(JsonViewTestCase, self).setUp()
        self.view = api.content.get_view(
            u'glossary',
            self.portal,
            self.request
        )

    def test_get_json_entries(self):
        self.assertEqual(
            self.view.get_json_entries(),
            [{'description': 'First Synonym Description',
              'synonym': 'First Synonym'},
             {'description': 'First Term Description', 'term': 'First Term'},
             {'description': 'Second Synonym Description',
              'synonym': 'Second Synonym'},
             {'description': 'Second Term Description', 'term': 'Second Term'}]
        )

    def test__call__(self):
        import json

        self.view()
        result = self.view.request.response.getBody()
        self.assertEqual(
            json.loads(result),
            [{'description': 'First Synonym Description',
              'synonym': 'First Synonym'},
             {'description': 'First Term Description', 'term': 'First Term'},
             {'description': 'Second Synonym Description',
              'synonym': 'Second Synonym'},
             {'description': 'Second Term Description', 'term': 'Second Term'}]
        )
