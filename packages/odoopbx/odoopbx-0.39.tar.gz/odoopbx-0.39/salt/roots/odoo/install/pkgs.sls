{% import_yaml "odoo/defaults.yaml" as defaults %}
{% set odoo = salt['pillar.get']('odoo', defaults.odoo, merge=True) %}

odoo-upgrade-pip:
  cmd.run:
    - name: pip3 install --upgrade pip

odoo-pkgs:
  pkg.installed:
    - pkgs:
      - git
      - subversion
      - python3-pip
      - build-essential
      - python3-dev
      - python3-babel
      - python3-git
      - python3-psycopg2
      - python3-venv
      - python3-wheel
      - python3-gevent
      - python3-greenlet
      - python3-eventlet
      - libxslt1-dev
      - libzip-dev
      - libldap2-dev
      - libsasl2-dev
      - python3-setuptools
      - node-less
      - python3-libxml2
      - python3-psutil
      - python3-ldap
      - python3-pypdf2
      - python3-vatnumber
      - python3-vobject
      - python3-ofxparse
      - python3-mako
      - python3-feedparser
      - python3-passlib
