include:
  - system
  - postgres
{% if not grains.virtual == "container" %}
  - asterisk
  - odoo
  - caddy
  - agent
{% endif %}
