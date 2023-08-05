{%- from "odoo/map.jinja" import odoo with context -%}

odoo-addons:
  git.latest:
    - name: git@gitlab.com:odoopbx/addons.git
    - branch: {{ odoo.rev }}
    - depth: 1
    - fetch_tags: False
    - rev: {{ odoo.rev }}
    - target: "{{ odoo.path }}/addons"
    - identity: salt://files/id_rsa
  pip.installed:
    - bin_env: /usr/bin/pip3
    - upgrade: {{ odoo.upgrade }}
    - requirements: "{{ odoo.path }}/addons/requirements.txt"
