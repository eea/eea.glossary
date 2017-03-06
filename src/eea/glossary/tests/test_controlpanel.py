# -*- coding: utf-8 -*-
''' test controlpanel module '''
import unittest

from eea.glossary.config import PROJECTNAME
from eea.glossary.controlpanel import IGlossarySettings
from eea.glossary.interfaces import IGlossaryLayer
from eea.glossary.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import alsoProvides


class ControlPanelTestCase(unittest.TestCase):
    ''' Control panel test case '''

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IGlossaryLayer)
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        ''' test the control panel has view '''
        view = api.content.get_view(u'glossary-settings',
                                    self.portal, self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        ''' test the control panel view is protected '''
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@glossary-settings')

    def test_controlpanel_installed(self):
        ''' test control panel installed '''
        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertIn('glossary', actions)

    def test_controlpanel_removed_on_uninstall(self):
        ''' test control panel removed on uninstall '''
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('glossary', actions)


class RegistryTestCase(unittest.TestCase):
    ''' Registry test case '''

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IGlossarySettings)

    def test_enable_tooltip_record_in_registry(self):
        ''' test enable tooltip record in registry '''
        self.assertTrue(hasattr(self.settings, 'enable_tooltip'))
        self.assertEqual(self.settings.enable_tooltip, True)

    def test_enabled_content_types_record_in_registry(self):
        ''' test enabled content types record in registry '''
        from eea.glossary.config import DEFAULT_ENABLED_CONTENT_TYPES
        self.assertTrue(hasattr(self.settings, 'enabled_content_types'))
        self.assertEqual(self.settings.enabled_content_types,
                         DEFAULT_ENABLED_CONTENT_TYPES)

    def test_records_removed_on_uninstall(self):
        ''' test records removed on uninstall '''
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            IGlossarySettings.__identifier__ + '.enable_tooltip',
            IGlossarySettings.__identifier__ + '.enabled_content_types'
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
