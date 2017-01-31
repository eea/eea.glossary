import json
import os.path
from z3c.relationfield import RelationValue
from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone.dexterity.utils import createContentInContainer
from eea.glossary.logger import logger

GLOSSARIES = [('eea-glossary', 'EEA Glossary'),
              ('eper', 'EPER'),
              ('eper2', 'EPER2')]

ALISS = [('aoa-glossary', 'AoA Glossary'),
         ('biodivspecies', 'Biodivspecies'),
         ('chm-biodiversity', 'CHM Biodiversity'),
         ('chm-biodiversity-coverage', 'CHM Biodiversity Coverage'),
         ('destinet', 'Destinet'),
         ('eea-highlights', 'EEA Highlights'),
         ('eea-terms', 'EEA Terms'),
         ('epanet-glossary', 'EPANET Glossary'),
         ('gemet', 'GEMET'),
         ('gemet-themes', 'GEMET Themes'),
         ('h2020', 'H2020'),
         ('semide', 'SEMIDE')]

# Skipped props are empty in all glossaries in all records
# or don't need to be imported, like center_parent, id, meta_type
# and all translations
ALISS_PROPS = [('definition', 'description'),
               ('name', 'title'),
               ('url', 'definition_source_url')]


def json_path(filename):
    return os.path.join(os.path.dirname(__file__), 'json_files', filename)


def import_from_json(self):
    site = self.aq_parent.SITE
    wftool = site.portal_workflow
    for g_id, g_title in GLOSSARIES:
        glossary = getattr(site, g_id, None)
        if not glossary:
            glossary = createContentInContainer(site, 'Glossary',
                                                title=g_title)
            wftool.doActionFor(glossary, 'publish')
        if glossary.objectValues():
            logger.info('Glossary % not empty, import cancelled' % g_title)
            continue
        data = json.load(open(json_path('%s.json' % g_id.replace('-', ''))))
        term_count = 0
        for term_id, term in data['EEA Glossary Term'].items():
            if not term['name']:
                continue
            publication_year = term['definition_source_publ_year']
            if not publication_year:
                publication_year = None
            ob = createContentInContainer(
                glossary, 'Term',
                title=term['name'],
                organisation_fullname=term[
                    'definition_source_org_fullname'],
                definition_source_publication=term[
                    'definition_source_publ'],
                subjects=[subject['code'] for subject in term['subjects']],
                definition_source_url=term['definition_source_url'],
                context=term['el_context'],
                publication_year=publication_year,
                qa_needed=term['QA_needed'] in [1, u'on'],
                long_definition=term['long_definition'],
                organisation=term['definition_source_org'],
                source=term['source'],
                description=term['definition'])
            term_count += 1
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
        logger.info('Imported %s synonyms into glossary %s' % (synonym_count,
                                                               g_title))

    for g_id, g_title in ALISS:
        glossary = getattr(site, g_id, None)
        if not glossary:
            glossary = createContentInContainer(site, 'Glossary',
                                                title=g_title)
            wftool.doActionFor(glossary, 'publish')
        if glossary.objectValues():
            logger.info('Glossary % not empty, import cancelled' % g_title)
            continue
        data = json.load(open(json_path('%s.json' % g_id)))
        term_count = 0
        for term_id, term in data.items():
            if not term['name']:
                continue
            ob = createContentInContainer(
                glossary, 'Term',
                title=term['name'],
                description=term['definition'],
                definition_source_url=term['url'])
            term_count += 1
            wftool.doActionFor(ob, 'publish')
        logger.info('Imported %s terms into glossary %s' % (term_count,
                                                            g_title))
