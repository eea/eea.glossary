# -*- coding: utf-8 -*-
''' setuphandlers module '''
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    ''' Hidden Profiles '''

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'eea.glossary:uninstall',
        ]
