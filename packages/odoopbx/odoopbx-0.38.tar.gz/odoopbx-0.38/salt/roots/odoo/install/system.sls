{%- from "odoo/map.jinja" import odoo with context -%}

odoo-user:
  user.present:
    - name: {{ odoo.user }}
    - shell: /bin/bash
    - home: "{{ odoo.path }}/data"
    - system: True
    - usergroup: True
  postgres_user.present:
    - name: {{ odoo.user }}
    - createdb: True
    - encrypted: True
    - db_user: postgres

odoo-folders:
  file.directory:
    - name: "{{ odoo.path }}/data"
    - user: {{ odoo.user}}
    - makedirs: True
    - mode: 700

odoo-configs:
  file.managed:
    - names:
      - {{ odoo.path }}/odoo.conf:
        - source: salt://odoo/templates/odoo.conf
        - group: {{ odoo.user }}
        - mode: 640
      - /etc/systemd/system/{{ odoo.odoover }}.service:
        - source: salt://odoo/templates/odoo.service
    - user: root
    - mode: 644
    - template: jinja
    - context: {{ odoo }}
    - backup: minion
    - require:
      - file: odoo-folders

odoo-init:
  cmd.run:
    - name: {{ odoo.path }}/odoo/odoo-bin -c {{ odoo.path }}/odoo.conf --no-http --stop-after-init  -i asterisk_base_sip,asterisk_calls_crm
    - runas: {{ odoo.user }}
    - shell: /bin/bash
    - unless: echo "env['asterisk_base.server']" | {{ odoo.path }}/odoo/odoo-bin shell -c {{ odoo.path }}/odoo.conf --no-http
{% if grains.virtual != "container" %}
odoo-service-running:
  service.running:
    - name: {{ odoo.odoover }}
    - enable: True
{% endif %}
