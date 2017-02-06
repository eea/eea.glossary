import json
import os.path
import logging
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone.dexterity.utils import createContentInContainer
from eea.glossary.logger import logger as glossary_logger

GLOSSARIES = [('eea-glossary', 'EEA Glossary',
              'http://glossary.eea.europa.eu/EEAGlossary'),
              ('eper-pollution-register-glossary',
               'EPER Pollution register glossary',
               'http://www.eper.ec.europa.eu/eper/glossary.asp'),
              ('eper-chemicals-glossary', 'EPER Chemicals glossary',
               'http://www.eper.ec.europa.eu/eper/glossary.asp')]

ALISS = [
    ('ee-aoa-glossary', 'EE-AoA Glossary',
     'http://aoa.ew.eea.europa.eu/database/acronyms'),
    ('european-species-listed-under-article',
     'European species listed under Article 17 of the Habitat Directive',
     'http://biodiversity.eionet.europa.eu/article17'),
    ('chm-biodiversity', 'CHM Biodiversity',
     'http://biodiversity-chm.eea.europa.eu/nyglossary_terms'),
    ('chm-biodiversity-coverage', 'CHM Biodiversity Coverage',
     'http://biodiversity-chm.eea.europa.eu/nyglossary_coverage'),
    ('sustainable-tourism-acronyms-destinet',
     'Sustainable Tourism Acronyms - DestiNet',
     'http://destinet.eu/database/acronyms'),
    ('eea-highlights', 'EEA Highlights',
     'http://www.eea.europa.eu/highlights'),
    ('other-eea-terms', 'Other EEA Terms',
     'http://www.eea.europa.eu/help/all-terms'),
    ('epanet-glossary-of-acronyms', 'EPANET Glossary of Acronyms',
     'http://epanet.ew.eea.europa.eu/database/acronyms'),
    ('gemet-themes-and-groups', 'GEMET Themes and Groups',
     'http://www.eionet.europa.eu/gemet'),
    ('gemet-environmental-thesaurus', 'GEMET - Environmental thesaurus',
     'http://www.eionet.europa.eu/gemet'),
    ('horizon2020-glossary', 'Horizon2020 Glossary',
     'http://coordination.h2020.net/database/acronyms'),
    ('semide-emwis-thesaurus', 'SEMIDE/EMWIS thesaurus',
     'http://www.semide.net/portal_thesaurus')]

# Skipped props are empty in all glossaries in all records
# or don't need to be imported, like center_parent, id, meta_type
# and all translations
ALISS_PROPS = [('definition', 'description'),
               ('name', 'title'),
               ('url', 'definition_source_url')]


logger = logging.getLogger('Plone')

def json_path(filename):
    return os.path.join(os.path.dirname(__file__), 'json_files', filename)


def import_from_json(self):
    site = self.aq_parent.SITE
    glossary_parent = site.help.glossary
    wftool = site.portal_workflow
    for g_id, g_title, url in GLOSSARIES:
        glossary = getattr(glossary_parent, g_id, None)
        if not glossary:
            glossary = createContentInContainer(glossary_parent, 'Glossary',
                                                title=g_title)
            wftool.doActionFor(glossary, 'publish')
        if glossary.objectValues():
            logger.info('Glossary %s not empty, import cancelled' % g_title)
            continue
        data = json.load(open(json_path('%s.json' % g_id)))
        term_count = 0
        for term_id, term in data['EEA Glossary Term'].items():
            if not term['name']:
                continue
            try:
                publication_year = int(term['definition_source_publ_year'])
                if not publication_year:
                    publication_year = None
            except:
                publication_year = None
            ob = createContentInContainer(
                glossary, 'Term',
                title=term['name'],
                organisation_fullname=term[
                    'definition_source_org_fullname'],
                definition_source_publication=term[
                    'definition_source_publ'],
                subjects=[subject['code'] for subject in term['subjects']],
                definition_source_url=term['definition_source_url'] or url,
                context=term['el_context'],
                publication_year=publication_year,
                long_definition=term['long_definition'],
                organisation=term['definition_source_org'],
                source=term['source'] or g_title,
                description=term['definition'])
            term_count += 1
            logger.info('%s imported out of %s (%s)' % (
                term_count, len(data['EEA Glossary Term'].items()), g_id))
            if term.get('approved'):
                wftool.doActionFor(ob, 'publish')
            data['EEA Glossary Term'][term_id]['new_id'] = ob.getId()
        logger.info('Imported %s terms into glossary %s' % (term_count,
                                                            g_title))
        intids = getUtility(IIntIds)
        synonym_count = 0
        for synonym_id in data['EEA Glossary Synonym']:
            synonym = data['EEA Glossary Synonym'][synonym_id]
            term_id = synonym['synonyms'][0].rsplit('/', 1)[-1]
            new_id = data['EEA Glossary Term'][term_id]['new_id']
            term = getattr(glossary, new_id)
            ob = createContentInContainer(
                glossary, 'Synonym', title=synonym['name'],
                term=RelationValue(intids.getId(term)))
            synonym_count += 1
            logger.info('%s synonyms imported out of %s (%s)' % (
                synonym_count,
                len(data['EEA Glossary Synonym'].items()),
                g_id))
        logger.info('Imported %s synonyms into glossary %s' % (synonym_count,
                                                               g_title))

    for g_id, g_title, url in ALISS:
        glossary = getattr(glossary_parent, g_id, None)
        if not glossary:
            glossary = createContentInContainer(glossary_parent, 'Glossary',
                                                title=g_title)
            wftool.doActionFor(glossary, 'publish')
            logger.info('%s Glossary created' %g_id)
        if glossary.objectValues():
            logger.info('Glossary %s not empty, import cancelled' % g_title)
            continue
        data = json.load(open(json_path('%s.json' % g_id)))
        term_count = 0
        for term_id, term in data.items():
            # there is a very strange issue with one record, with name 'path'
            if not term['name'] or term['name'] == u'path':
                continue
            ob = createContentInContainer(
                glossary, 'Term',
                title=term.get('name'),
                description=term.get('definition'),
                definition_source_url=term.get('url') or url,
                source=term.get('source') or g_title)
            term_count += 1
            logger.info('%s terms imported out of %s (%s)' % (
                term_count, len(data.items()), g_id))
            wftool.doActionFor(ob, 'publish')
        logger.info('Imported %s terms into glossary %s' % (term_count,
                                                            g_title))
