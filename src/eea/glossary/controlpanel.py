# -*- coding: utf-8 -*-
from eea.glossary import _
from eea.glossary.interfaces import IGlossarySettings
from plone.app.registry.browser import controlpanel


class GlossarySettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IGlossarySettings
    label = _(u'Glossary')
    description = _(u'Settings for the eea.glossary package')


class GlossarySettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = GlossarySettingsEditForm
