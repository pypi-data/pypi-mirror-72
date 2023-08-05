ipset_whitelist:
  ipset.set_present:
    - set_type: hash:net
    - name: whitelist
    - comment: True
    - counters: True


ipset_blacklist:
  ipset.set_present:
    - set_type: hash:net
    - name: blacklist
    - comment: True
    - counters: True
    - timeout: 3600

voip_chain:
  iptables.chain_present:
    - name: voip

{% for port in ['5060', '65060'] %}
port_{{ port }}:
  iptables.insert:
    - position: 1
    - table: filter
    - family: ipv4
    - chain: INPUT
    - jump: voip
    - dport: {{ port }}
    - proto: udp
{% endfor %}

whitelist:
  iptables.append:
    - chain: voip
    - match-set: whitelist src
    - jump: ACCEPT

blacklist:
  iptables.append:
    - chain: voip
    - match-set: blacklist src
    - jump: DROP

{% for agent in ['VaxSIPUserAgent', 'friendly-scanner', 'sipvicious', 'sipcli'] %}
scanner_{{ agent }}:
  iptables.append:
    - chain: voip
    - match: udp
    - match: string
    - string: {{ agent }}
    - algo: bm
    - to: 65535
    - jump: DROP
{% endfor %}
