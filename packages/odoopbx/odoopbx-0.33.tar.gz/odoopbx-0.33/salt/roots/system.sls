system-python-apt:
  cmd.run:
    - names:
      - dpkg -l python-apt python3-apt python3-git iptables ipset
      - apt -y update && apt -y install python-apt python3-apt python3-git iptables ipset
