# -*- coding: utf-8 -*-
import json
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from Products.Five.browser import BrowserView

from plone import api
from plone.i18n.normalizer.base import baseNormalize
from plone.memoize import ram
from zc.relation.interfaces import ICatalog

from eea.glossary.interfaces import IGlossarySettings
from eea.glossary.interfaces import subjects


def _catalog_counter_cachekey(method, self):
    """Return a cachekey based on catalog updates."""

    catalog = api.portal.get_tool('portal_catalog')
    return str(catalog.getCounter())


class TermView(BrowserView):

    """Default view for Term type"""

    def __call__(self, **kwargs):
        self.request.set('skipRelations', 1)
        return self.index()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_entry(self):
        """Get term in the desired format"""

        item = {
            'title': self.context.title,
            'description': self.context.description,
            'source': self.context.source,
            'context': self.context.context,
            'comment': self.context.comment,
            'definition_source_publication':
                self.context.definition_source_publication,
            'publication_year': self.context.publication_year,
            'definition_source_url': self.context.definition_source_url,
            'organisation': self.context.organisation,
            'organisation_fullname': self.context.organisation_fullname,
            'subjects': self.context.subjects,
            'disabled': self.context.disabled,
            'long_definition': self.context.long_definition,
            'qa_needed': self.context.qa_needed,
        }
        return item

    def get_synonyms(self, attribute_name='term'):
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        query = dict(
            to_id=intids.getId(aq_inner(self.context)),
            from_attribute=attribute_name
        )

        relations = list(catalog.findRelations(query))

        for rel in relations:
            obj = intids.queryObject(rel.from_id)
            if obj is not None and checkPermission('zope2.View', obj):
                # we can also append the obj itself
                result.append(rel)
        return result

    def get_subject_title(self, subject_id):
        return subjects.by_value.get(subject_id).title


class SynonymView(BrowserView):

    """Default view for Synonym type"""

    def __call__(self, **kwargs):
        self.request.set('skipRelations', 1)
        return self.index()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_entry(self):
        """Get synonym in the desired format"""

        item = {
            'title': self.context.title,
            'description': self.context.description,
            'term': self.context.term,
        }
        return item

    def get_subject_title(self, subject_id):
        return subjects.by_value.get(subject_id).title


class GlossaryView(BrowserView):

    """Default view of Glossary type"""

    def __call__(self, **kwargs):
        self.request.set('skipRelations', 1)
        return self.index()

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @ram.cache(_catalog_counter_cachekey)
    def get_entries(self):
        """Get glossary entries and keep them in the desired format"""

        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        query = dict(portal_type=['Term', 'Synonym'],
                     path={'query': path, 'depth': 1})

        items = {}
        for brain in catalog(**query):
            obj = brain.getObject()
            try:
                index = baseNormalize(obj.title)[0].upper()
            except IndexError:
                index = baseNormalize(obj.title).upper()
            if index not in items:
                items[index] = []
            item = {
                'title': obj.title,
                'description': obj.description,
            }
            items[index].append(item)

        keys = items.keys()
        for k in keys:
            items[k] = sorted(
                items[k],
                key=lambda term: term['title']
            )

        return items

    def letters(self):
        """Return all letters sorted"""
        return sorted(self.get_entries().keys())

    def terms(self, letter):
        """Return all terms of one letter"""
        return self.get_entries()[letter]


class GlossaryStateView(BrowserView):
    """Glossary State view used to enable or disable resources

    This is called by JS and CSS resources registry
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def tooltip_is_enabled(self):
        """Check if term tooltip is enabled."""
        return api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enable_tooltip')

    @property
    def content_type_is_enabled(self):
        """Check if we must show the tooltip in this context."""
        portal_type = getattr(self.context, 'portal_type', None)
        enabled_content_types = api.portal.get_registry_record(
            IGlossarySettings.__identifier__ + '.enabled_content_types')
        return portal_type in enabled_content_types

    @property
    def is_view_action(self):
        """Check if we are into the view action."""
        context_url = self.context.absolute_url()
        # Check if use Virtual Host configuration (ex.: Nginx)
        request_url = self.request.get('VIRTUAL_URL', None)

        if request_url is None:
            request_url = self.request.base + self.request.get('PATH_INFO', '')

        if context_url == request_url:
            return True

        # Default view
        return context_url.startswith(request_url) and \
            len(context_url) > len(request_url)

    def __call__(self):
        return self.tooltip_is_enabled and \
            self.content_type_is_enabled and self.is_view_action


class JsonView(BrowserView):
    """Json view that return all glossary items in json format

    This view is used into an ajax call for
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @ram.cache(_catalog_counter_cachekey)
    def get_json_entries(self):
        """Get all itens and prepare in the desired format.
        Note: do not name it get_entries, otherwise caching is broken. """

        catalog = api.portal.get_tool('portal_catalog')

        items = []
        for brain in catalog(portal_type=['Term']):
            items.append({
                'term': brain.Title,
                'description': brain.Description,
            })
        for brain in catalog(portal_type=['Synonym']):
            items.append({
                'synonym': brain.Title,
                'description': brain.Description,
            })

        return items

    def __call__(self):
        response = self.request.response
        response.setHeader('content-type', 'application/json')

        return response.setBody(json.dumps(self.get_json_entries()))
