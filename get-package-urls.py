#!/usr/bin/env python3

# Parse the tenable agent download page and extract download links
# for multiple operating systems.
#
# Output is in YAML format and may be directly imported into Ansible, e.g.:
#
#   $ get-package-urls.py >vars/package_url.yaml
#
# TODO: Fetch checksums

import bs4
import http.client
import re
import sys

DOWNLOAD_HOST='www.tenable.com'
DOWNLOAD_URL='https://' + DOWNLOAD_HOST + '/downloads/api/v1/public/pages/nessus-agents/downloads/'
INDEX_URL='https://' + DOWNLOAD_HOST + '/downloads/nessus-agents?loginAttempted=true'

filename_patterns = {
   'Debian9':  'NessusAgent.*debian6_amd64.deb',
   'Debian10': 'NessusAgent.*debian6_amd64.deb',
   'RedHat6':  'NessusAgent.*es6.x86_64.rpm',
   'RedHat7':  'NessusAgent.*es7.x86_64.rpm',
   'CentOS7':  'NessusAgent.*es7.x86_64.rpm',
   'RedHat8':  'NessusAgent.*es8.x86_64.rpm',
   'SLES11':   'NessusAgent.*suse11.x86_64.rpm',
   'SLES12':   'NessusAgent.*suse12.x86_64.rpm',
   'SLES15':   'NessusAgent.*suse15.x86_64.rpm',
   'Ubuntu14': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu16': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu18': 'NessusAgent.*ubuntu1110_amd64.deb',
   'Ubuntu20': 'NessusAgent.*ubuntu1110_amd64.deb',
}

print('Downloading index page', file=sys.stderr)
conn = http.client.HTTPSConnection(DOWNLOAD_HOST)
conn.request('GET', INDEX_URL)
resp = conn.getresponse()

soup = bs4.BeautifulSoup(resp.read(), 'html.parser')

print('---')
print('package_url:')

# We loop multiple times through the page for each OS so we can give a warning
# if there is no match for an OS.

for os, pattern in filename_patterns.items():
    for link in soup.find_all('li', 'download-list-group-item'):
        filename_tag = link.find('span', 'file-name')
        filename = filename_tag.string

        if re.search(pattern, filename):
            size_tag = link.find('span', id=re.compile('size-[0-9]+'))
            download_id = size_tag['id'][5:]
            download_url = DOWNLOAD_URL + download_id + '/download?i_agree_to_tenable_license_agreement=true'
            print('  {}: {}'.format(os, download_url))
            break

    else:
        print('Warning: could not find package for ' + os, file=sys.stderr)

