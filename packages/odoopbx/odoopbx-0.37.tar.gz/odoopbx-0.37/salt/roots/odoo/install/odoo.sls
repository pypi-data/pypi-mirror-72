{%- from "odoo/map.jinja" import odoo with context -%}

odoo-pre-install:
  pip.installed:
    - bin_env: /usr/bin/pip3
    - pkgs:
      - werkzeug==0.14.1

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
    - ignore_installed: True
    - upgrade: {{ odoo.upgrade }}
    - requirements: "{{ odoo.path }}/odoo/requirements.txt"
