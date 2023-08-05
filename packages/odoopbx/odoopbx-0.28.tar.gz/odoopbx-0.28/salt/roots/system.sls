system-python-apt:
  cmd.run:
    - name: apt update && apt install python3-apt iptables ipset
    - unless: dpkg -l python3-apt iptables ipset
