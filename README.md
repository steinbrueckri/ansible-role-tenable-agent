# ansible-role-tenable-agent

Ansible role for installing and configuring Nessus Agent

## Role Variables

| Variable                    |                                                                                                                                         Description                                                                                                                                          |
| --------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| `nessus_agent_key`          |                                                                                                             key used for linking with nessus host (this is a required variable)                                                                                                              |
| `nessus_agent_group`        |                                                                                             host group this agent should be added to when linking with nessus host (this is a required variable)                                                                                             |
| `nessus_agent_host`         |                                                                                                                   nessus host to link with (default: `cloud.tenable.com`)                                                                                                                    |
| `nessus_agent_port`         |                                                                                                                              nessus host port (default: `443`)                                                                                                                               |
| `nessus_agent_rules`        |                                                                                                                    Object can be used to configure the nessusd.rules file                                                                                                                    |
| `nessus_agent_download_url` | Getting the download URL can be a bit tricky, just go to [https://www.tenable.com/downloads/nessus-agents](https://www.tenable.com/downloads/nessus-agents) and copy the URL, like in the example below. You need also to download the file and calculate the md5sum. _NOTE:_ The Link is nt |
| `nessus_agent_package`      |                                                                                                    can be either a repository package, path to a file, or a URL (default: `NessusAgent`)                                                                                                     |

_NOTE:_ The Tenable download URLs are not static and they will change. To automatically generate a new list, run

```sh
get-package-urls.py >vars/package_url.yaml
```

## Dependencies

None for the Ansible role. To run get-package-urls.py, install the Python `bs4` package.

## Example Playbook

### Simple use case

```yaml
- hosts: all

  vars:
    nessus_agent_key: xxxxxxxxx
    nessus_agent_file_checksum: "md5:3eeee6531c7822ac7fe374cc28d74779"
    nessus_agent_download_url: "https://www.tenable.com/downloads/api/v1/public/pages/nessus-agents/downloads/12176/download?i_agree_to_tenable_license_agreement=true" # NessusAgent-8.2.2-ubuntu1110_amd64.deb

  roles:
    - role: ansible-role-nessus-agent
```

### Advanced use case

```yaml
- hosts: all

  vars:
    nessus_agent_key: xxxxxxxxx
    nessus_agent_group: GCP
    nessus_agent_file_checksum: "md5:3eeee6531c7822ac7fe374cc28d74779"
    nessus_agent_download_url: "https://www.tenable.com/downloads/api/v1/public/pages/nessus-agents/downloads/12176/download?i_agree_to_tenable_license_agreement=true" # NessusAgent-8.2.2-ubuntu1110_amd64.deb
    nessus_agent_rules:
      default: accept
      plugin_reject:
        - 33851

  roles:
    - role: ansible-role-nessus-agent
```
