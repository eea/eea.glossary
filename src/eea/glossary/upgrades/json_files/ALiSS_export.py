''' This is the python script used in ZMI on
 http://glossary.eea.europa.eu/etds/ALiSS_catalog to export data from
 the catalog

 the query value (i.e. Glossary UID) must be taken for each ALiSS Center
 from manage_properties_html import.

 Commented, since it is not a valid module, can only be run in Zope console '''

'''query = {'meta_type': {'operator': 'and ', 'query': 'ALiSS Element'},
         'center_parent': {'query': '9385171863'}}
elements = {}
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
brains = context(query)
for k in brains:
    el_data = {}
    for prop in props:
        prop_value = getattr(k, prop)
        if prop_value:
            el_data[prop] = prop_value
    elements[k.id] = el_data
return elements'''
