agent-pkg:
  pkg.installed:
    - pkgs:
        - python3-click
        - python3-odoorpc
        - python3-panoramisk
        - python3-setproctitle
        - python3-terminado

agent-libs:
  pip.installed:
    - pkgs: [aiorun]

agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
    - template: jinja
{% if grains.virtual != "container" %}
  service:
    - running
    - name: odoopbx-agent
    - enable: True
{% endif %}
