# -*- coding: utf-8 -*-
''' test setup '''
import unittest

from eea.glossary.config import PROJECTNAME
from eea.glossary.testing import INTEGRATION_TESTING
from plone.browserlayer.utils import registered_layers


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        ''' test installed '''
        qi = self.portal['portal_quickinstaller']
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer(self):
        ''' test addon layer '''
        layers = [l.getName() for l in registered_layers()]
        self.assertIn('IGlossaryLayer', layers)

    def test_add_glossary_permission(self):
        ''' test add glossary permission '''
        permission = 'eea.glossary: Add Glossary'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_add_term_permission(self):
        ''' test add term permission '''
        permission = 'eea.glossary: Add Term'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    def test_add_synonym_permission(self):
        ''' test add synonym permission '''
        permission = 'eea.glossary: Add Synonym'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        ''' test uninstalled '''
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_addon_layer_removed(self):
        ''' test addon layer removed '''
        layers = [l.getName() for l in registered_layers()]
        self.assertNotIn('IGlossaryLayer', layers)
