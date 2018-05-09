#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from slugify import slugify
from jinja2 import Template

BASE_URL = 'https://tlv.serverlessdays.io/sessions/'

"""Replace the keys taken from Google Sheets csv with shorter ones"""
keys_normal = {
    'Speaker Name (English), as it would appear on our site': 'name',
    'Speaker title (e.g. CEO at Acme Corporation)': 'speaker_title',
    'A few words about yourself (Markdown for links)': 'speaker_description',
    'Full session description (Markdown for links)': 'session_description', 
    'Session title (32 chars max)': 'session_title', 
    'Session subtitle (80 chars max)': 'session_subtitle',
    'Preferred session duration': 'duration', 
    'Session language (we prefer English, if possible)': 'language',
    'Profile image': 'profile_image',
}

def normalize(d):
    """Replace the keys taken from Google Sheets csv with shorter ones,
    and add convenience members."""
    rv = {}
    for k in d:
        if k in keys_normal:
            rv[keys_normal[k]] = d[k]
        else:
            rv[k] = d[k]

    rv['url'] = slugify('{} {}'.format(rv['name'], rv['session_title']))
    rv['absolute_url'] = '{}{}.html'.format(BASE_URL, rv['url'])
    rv['profile_image_path'] = '{}-profile.jpg'.format(slugify(rv['name']))
    return rv

# CSV from Google Sheets
with open('sessions.csv', encoding='utf-8') as f:
    READER = csv.DictReader(f)
    SESSIONS = [normalize(session) for session in list(READER)]

# Session template
with open('html/sessions/template.jinja2', encoding='utf-8') as f:
    template = Template(f.read())

# Session list template
with open('html/sessions/sessions.jinja2', encoding='utf-8') as f:
    sessions_template = Template(f.read())


for session in SESSIONS:
    local_file_path = 'html/sessions/{}.html'.format(session['url'])
    print(session['session_subtitle'])
    with open(local_file_path, 'w', encoding='utf-8') as f:
        f.write(template.render(session))

local_file_path = 'html/sessions/sessions.html'
with open(local_file_path, 'w', encoding='utf-8') as f:
    f.write(sessions_template.render( locals() ))

absolute_urls = [ s['absolute_url'] for s in SESSIONS ]

print('\n'.join(absolute_urls))

