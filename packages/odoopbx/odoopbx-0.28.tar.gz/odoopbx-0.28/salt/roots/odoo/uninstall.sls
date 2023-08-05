{%- from "odoo/map.jinja" import odoo with context -%}

odoo-service-dead:
  service.dead:
    - name: {{ odoo.odoover }}
    - enable: False

odoo-files-absent:
  file.absent:
    - names:
      - {{ odoo.path }}
      - /etc/systemd/system/{{ odoo.odoover }}.service
      - /etc/caddy/Caddyfile.d/odoopbx.conf

odoo-user-absent:
  user.absent:
    - name: {{ odoo.user }}
