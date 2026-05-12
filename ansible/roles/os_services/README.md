Role Name
=========

A brief description of the role goes here.

Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

Operating Notes
---------------

### Unban an IP from the nginx-mtls jail

The `nginx-mtls` jail bans source IPs that complete the TLS handshake but fail client certificate verification (10 failures within 60 seconds → 1 hour ban). Typical trigger: a mobile client whose client certificate has expired retries in the background.

Unban a specific IP (e.g. after issuing a replacement client certificate):

    sudo fail2ban-client set nginx-mtls unbanip <ip>

Inspect current ban state:

    sudo fail2ban-client status nginx-mtls

Tuning lives in `files/fail2ban/jail.local`; the matching filter is `files/fail2ban/nginx-mtls.conf`.

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
