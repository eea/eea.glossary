import json
import codecs

# dict of all languages found in the old glossaries and their iso code
langs = {'Swedish': 'sv', 'Icelandic': 'is', 'Estonian': 'et', 'Turkish': 'tr',
         'Romanian': 'ro', 'Italian': 'it', 'Serbian': 'sr', 'Slovenian': 'sl',
         'Rhaeto-Romanic': 'rm', 'Dutch': 'nl', 'Faroese': 'fo',
         'Byelorussian': 'be', 'Danish': 'da', 'Bulgarian': 'bg',
         'Hungarian': 'hu', 'Catalan': 'ca', 'Lithuanian': 'lt',
         'Greenlandic': 'kl', 'French': 'fr', 'Norwegian': 'no',
         'Basque': 'eu', 'Russian': 'ru', 'Slovak': 'sk', 'Croatian': 'hr',
         'Macedonian': 'mk', 'Finnish': 'fi', 'Albanian': 'sq',
         'Scottish': 'gd', 'Maltese': 'mt', 'Latvian': 'lv', 'English': 'en',
         'Greek': 'el', 'Portuguese': 'pt', 'Irish': 'ga', 'Czech': 'cz',
         'German': 'de', 'Spanish': 'es', 'Polish': 'pl'}
glossaries = {'eeaglossary': 'EEAGlossary',
              'eper': 'EPER',
              'eper2': 'EPER2'}
BASE_URL = 'http://glossary.eea.europa.eu/'

for json_id, glossary_id in glossaries.items():
    data = json.load(open('%s.json' % json_id))
    namespaces = [
        'xmlns:wf="http://intelleo.eu/ontologies/workflow/ns#"',
        'xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"',
        'xmlns:eea="http://www.eea.europa.eu/ontologies.rdf#"',
        'xmlns:owl="http://www.w3.org/2002/07/owl#"',
        'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
        'xmlns:dcat="http://www.w3.org/ns/dcat#"',
        'xmlns:term="http://www.eea.europa.eu/portal_types/Term#"',
        'xmlns:synonym="http://www.eea.europa.eu/portal_types/Synonym#"',
        'xmlns:dcterms="http://purl.org/dc/terms/"',
        'xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"',
        'xmlns:schema="http://schema.org/"'
    ]
    f = codecs.open('%s.rdf' % json_id, 'w', 'utf-8')
    f.write('<?xml version="1.0"?>\n')
    f.write('<rdf:RDF ' + ' '.join(namespaces) + ' >\n')
    for term_id, term in data['EEA Glossary Term'].items():
        orig_url = (BASE_URL + glossary_id + '/' +
                    term_id[0].upper() + '/' + term_id)
        f.write('    <term:Term rdf:about="%s">\n' % orig_url)
        f.write('        <dcterms:isPartOf rdf:resource="%s%s" />\n' %
                (BASE_URL, glossary_id))
        f.write('        <dcterms:title xml:lang="en">%s</dcterms:title>\n' %
                term['name'].replace('<', '&lt;').replace('>', '&gt;'))
        for lang, code in langs.items():
            if term.get(lang):
                f.write(
                    '        <dcterms:title xml:lang="%s">%s</dcterms:title>\n'
                    % (code,
                       term[lang].replace('<', '&lt;').replace('>', '&gt;')))
        f.write(
            '        <term:organisation_fullname>%s'
            '</term:organisation_fullname>\n'
            % term['definition_source_org_fullname'])
        f.write(
            '        <term:definition_source_publication>' +
            term['definition_source_publ'] +
            '</term:definition_source_publication>\n'
        )
        for subject in term['subjects']:
            f.write(
                '        <term:subjects>%s</term:subjects>\n'
                % subject['code'])
        f.write(
            '        <term:definition_source_url>' +
            term['definition_source_url'] +
            '</term:definition_source_url>\n'
        )
        f.write(
            '        <term:context>%s</term:context>\n' % term['el_context'])
        f.write(
            '        <term:publication_year>' +
            term['definition_source_publ_year'] +
            '</term:publication_year>\n'
        )
        f.write(
            '        <term:qa_needed>%s</term:qa_needed>\n' %
            str(term['QA_needed'] in [1, 'on']))
        f.write(
            '        <term:long_definition>%s</term:long_definition>\n' %
            term['long_definition'])
        f.write(
            '        <term:organisation>%s</term:organisation>\n'
            % term['definition_source_org'])
        f.write('        <term:source>%s</term:source>\n' % term['source'])
        f.write('    </term:Term>\n')
    for term_id, term in data['EEA Glossary Synonym'].items():
        orig_url = (BASE_URL + glossary_id + '/' +
                    term_id[0].upper() + '/' + term_id)
        f.write('    <synonym:Synonym rdf:about="%s">\n' % orig_url)
        f.write('        <dcterms:isPartOf rdf:resource="%s%s" />\n' %
                (BASE_URL, glossary_id))
        f.write('        <dcterms:title xml:lang="en">%s</dcterms:title>\n' %
                term['name'].replace('<', '&lt;').replace('>', '&gt;'))
        f.write('        <synonym:synonyms rdf:resource="%s/%s" />\n'
                % (BASE_URL, term['synonyms'][0]))
        f.write('    </synonym:Synonym>\n')
    f.write('</rdf:RDF>')


def escape(text):
    return text.replace('<', '&lt;').replace('>', '&gt;')
