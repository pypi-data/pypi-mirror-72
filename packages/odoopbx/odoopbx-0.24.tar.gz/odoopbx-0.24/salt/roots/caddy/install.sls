# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "caddy/map.jinja" import caddy with context %}

caddy-pkg-deps:
  pkg.installed:
    - pkgs: {{ caddy.pkgs }}

{{ caddy.bindir }}:
  file.directory:
    - state: present
    - mode: 755

caddy-download:
  archive.extracted:
    - name: {{ caddy.bindir }}
    - failhard: True
    - source: 'https://caddyserver.com/download/linux/amd64?license=personal&telemetry=off'
    - archive_format: tar
    - skip_verify: true
    - enforce_toplevel: false
    - options: '--exclude=init/ --exclude=README.txt --exclude=LICENSES.txt --exclude=CHANGES.txt'
    - overwrite: {{ caddy.force_update }}

caddy-setcap:
  cmd.run:
    - name: setcap 'cap_net_bind_service=+ep' {{ caddy.bindir }}/caddy
    - unless: getcap {{ caddy.bindir }}/caddy | grep -q 'cap_net_bind_service+ep'

caddy-identity:
  user.present:
    - name: www-data
    - uid: 33
    - gid: 33

caddy-ssl-dir:
  file.directory:
    - name: /etc/ssl/caddy
    - user: www-data
    - group: www-data
    - mode: 700
    - require:
      - user: caddy-identity

caddy-conf-default:
  file.managed:
    - name: /etc/caddy/Caddyfile
    - replace: False
    - makedirs: True
    - contents: "import Caddyfile.d/*.conf"

caddy-conf-import:
  file.replace:
    - name: /etc/caddy/Caddyfile
    - pattern: "^import .*Caddyfile.d/.*"
    - repl: "import Caddyfile.d/*.conf"
    - append_if_not_found: True

caddy-service:
  file.managed:
    - name: /etc/systemd/system/caddy.service
    - source: salt://caddy/caddy.service
    - user: root
    - group: root
    - mode: 0664
    - replace: {{ caddy.force_update }}
    - backup: minion
  service.running:
    - name: caddy
    - enable: {{ caddy.service_enable }}
    - require:
      - file: caddy-service
