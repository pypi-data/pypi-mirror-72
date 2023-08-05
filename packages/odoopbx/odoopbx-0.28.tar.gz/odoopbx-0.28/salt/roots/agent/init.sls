agent-service:
  file:
    - managed
    - name: /etc/systemd/system/odoopbx-agent.service
    - source: salt://agent/agent.service
    - template: jinja
  service:
    - running
    - name: odoopbx-agent
    - enable: True
