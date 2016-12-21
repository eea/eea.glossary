import simplejson as json
for glo_id in ['EPER', 'EPER2', 'EEAGlossary']:
    glo = getattr(app, glo_id)
    data = {'EEA Glossary Element': {}, 'EEA Glossary Synonym': {}}
    for fol in glo.objectValues('EEA Glossary Folder'):
        for el in fol.objectValues(['EEA Glossary Element',
                                    'EEA Glossary Synonym']):
            el_id = el.getId()
            data[el.meta_type][el_id] = el.__dict__
            if glo_id == 'EEAGlossary':
                data[el.meta_type][el_id]['definition'] = el.definition.decode(
                    'latin1')
                data[el.meta_type][el_id][
                    'definition_source_publ'
                ] = el.definition_source_publ.decode('latin1')
                if hasattr(el, 'English'):
                    data[el.meta_type][el_id]['English'] = el.English.decode(
                        'latin1')
                for lang in el.history:
                    for lang_data in el.history[lang]:
                        count = 0
                        if not isinstance(el.history[lang][count]['trans'],
                                          unicode):
                            data[el.meta_type][el_id]['history'][lang][count][
                                'trans'] = el.history[lang][count][
                                    'trans'].decode('latin1')
                        count += 1
        filename = '/var/local/ZopeInstances/Forum/%s.json' % glo_id
        with open(filename, 'wb') as f:
            f.write(json.dumps(data))
