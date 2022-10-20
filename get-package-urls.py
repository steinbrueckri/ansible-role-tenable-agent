#!/usr/bin/env python3

# Parse the tenable agent download page and extract download links
# for multiple operating systems.
#
# Output is in YAML format and may be directly imported into Ansible, e.g.:
#
#   $ get-package-urls.py >vars/package_url.yaml

import bs4
import http.client
import json
import re
import sys

DOWNLOAD_HOST = 'www.tenable.com'
DOWNLOAD_URL  = 'https://' + DOWNLOAD_HOST + '/downloads/api/v1/public/pages/nessus-agents/downloads/'
INDEX_URL     = 'https://' + DOWNLOAD_HOST + '/downloads/nessus-agents?loginAttempted=true'

filename_patterns = {
   'Debian9':  'NessusAgent.*debian9_amd64.deb',
   'Debian10': 'NessusAgent.*debian9_amd64.deb',
   'Debian11': 'NessusAgent.*debian9_amd64.deb',
   'RedHat6':  'NessusAgent.*es6.x86_64.rpm',
   'RedHat7':  'NessusAgent.*es7.x86_64.rpm',
   'CentOS7':  'NessusAgent.*es7.x86_64.rpm',
   'RedHat8':  'NessusAgent.*es8.x86_64.rpm',
   'CentOS8':  'NessusAgent.*es8.x86_64.rpm',
   'SLES11':   'NessusAgent.*suse11.x86_64.rpm',
   'SLES12':   'NessusAgent.*suse12.x86_64.rpm',
   'SLES15':   'NessusAgent.*suse15.x86_64.rpm',
   'Ubuntu14': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu16': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu18': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu20': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu22': 'NessusAgent.*ubuntu1110_amd64.deb',   
}

print('Downloading index page', file=sys.stderr)
conn = http.client.HTTPSConnection(DOWNLOAD_HOST)
conn.request('GET', INDEX_URL)
resp = conn.getresponse()

if resp.status != 200:
    print('Error {} retrieving index page: {}'.format(resp.status, resp.reason))
    sys.exit(1)

soup = bs4.BeautifulSoup(resp.read(), 'html.parser')

script = soup.find('script', id='__NEXT_DATA__')
if script is None:
    print('Error: could not find <script> containing the data')
    sys.exit(1)

data = json.loads(script.string)
downloads = data['props']['pageProps']['page']['downloads']

packages = {}

for os, pattern in filename_patterns.items():
    for dl in downloads:
        dl_id       = dl['id']
        dl_filename = dl['file']
        dl_checksum = dl['meta_data']['md5']

        if re.search(pattern, dl_filename):
            dl_url = DOWNLOAD_URL + str(dl_id) + '/download?i_agree_to_tenable_license_agreement=true'
            packages[os] = {
                'url':      dl_url,
                'checksum': dl_checksum
            }
            break
    else:
        print('Warning: could not find package for ' + os, file=sys.stderr)

print('---')
print('package_url:')
for os, pkg in packages.items():
    print('  {}: {}'.format(os, pkg['url']))

print()
print('package_checksum:')
for os, pkg in packages.items():
    print('  {}: md5:{}'.format(os, pkg['checksum']))

