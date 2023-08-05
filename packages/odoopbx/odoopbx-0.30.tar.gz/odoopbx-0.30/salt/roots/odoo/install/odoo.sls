{%- from "odoo/map.jinja" import odoo with context -%}

odoo-install:
  git.latest:
    - name: https://github.com/odoo/odoo.git
    - branch: {{ odoo.rev }}
    - rev: {{ odoo.rev }}
    - target: "{{ odoo.path }}/odoo"
    - depth: 1
    - fetch_tags: False
  pip.installed:
    - bin_env: /usr/bin/pip3
    # Do we need to force_reinstall? Do we still have "Cannot uninstall 'greenlet'. It is a distutils installed project ..."
    # - force_reinstall: True
    - ignore_installed: True
    - upgrade: {{ odoo.upgrade }}
    - requirements: "{{ odoo.path }}/odoo/requirements.txt"
