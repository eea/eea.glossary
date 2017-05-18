# -*- coding: utf-8 -*-
"""Setup testing infrastructure.

For Plone 5 we need to install plone.app.contenttypes.
"""
import pkg_resources

from plone import api
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE \
        as PLONE_FIXTURE

IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):
    ''' Setup fixtures '''

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        ''' Setup Zope '''
        import eea.glossary
        self.loadZCML(package=eea.glossary)

    def setUpPloneSite(self, portal):
        ''' Setup Plone site '''
        self.applyProfile(portal, 'eea.glossary:default')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='eea.glossary:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='eea.glossary:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='eea.glossary:Robot',
)
