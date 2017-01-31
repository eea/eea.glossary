# Script used to check which properties from the json have useful values
# and need to be imported.

import json

file_ids = ['AoAGlossary.json', 'biodivspecies.json',
            'CHMBiodiversityCoverage.json', 'CHMBiodiversity.json',
            'destinet.json', 'EEAHighlights.json', 'EEATerms.json',
            'EPANETGlossary.json', 'GEMET.json', 'GEMETThemes.json',
            'h2020.json', 'SEMIDE.json']
props = [
    'center_parent', 'center_uid', 'definition', 'elem_parent', 'g_server',
    'google_enable', 'google_error', 'google_parent', 'group_id', 'id',
    'meta_type', 'name', 'objectname_ar', 'objectname_bg', 'objectname_cs',
    'objectname_da', 'objectname_de', 'objectname_el', 'objectname_en',
    'objectname_en-us', 'objectname_es', 'objectname_et', 'objectname_eu',
    'objectname_fi', 'objectname_fr', 'objectname_hu', 'objectname_is',
    'objectname_it', 'objectname_lt', 'objectname_lv', 'objectname_mt',
    'objectname_nl', 'objectname_no', 'objectname_pl', 'objectname_pt',
    'objectname_ro', 'objectname_ru', 'objectname_sk', 'objectname_sl',
    'objectname_sv', 'objectname_tr', 'objecttrans_ar', 'objecttrans_bg',
    'objecttrans_cs', 'objecttrans_da', 'objecttrans_de', 'objecttrans_el',
    'objecttrans_en', 'objecttrans_en-US', 'objecttrans_en-us',
    'objecttrans_es', 'objecttrans_et', 'objecttrans_eu', 'objecttrans_fi',
    'objecttrans_fr', 'objecttrans_hu', 'objecttrans_is', 'objecttrans_it',
    'objecttrans_lt', 'objecttrans_lv', 'objecttrans_mt', 'objecttrans_nl',
    'objecttrans_no', 'objecttrans_pl', 'objecttrans_pt', 'objecttrans_ro',
    'objecttrans_ru', 'objecttrans_sk', 'objecttrans_sl', 'objecttrans_sv',
    'objecttrans_tr', 'page_snippet', 'page_title', 'page_url', 'url']

big_dict = {}
to_exclude = ['meta_type']
for file_id in file_ids:
    big_dict.update(json.load(open(file_id)))

for prop_id in props:
    for k, dictionar in big_dict.items():
        if dictionar.get(prop_id):
            if prop_id not in to_exclude:
                break
            elif dictionar[prop_id] != 'ALiSS Element':
                break
    else:
        print prop_id
