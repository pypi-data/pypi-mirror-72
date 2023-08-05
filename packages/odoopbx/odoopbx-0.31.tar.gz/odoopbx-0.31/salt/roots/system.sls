system-python-apt:
  cmd.run:
    - names:
      - dpkg -l python-apt python3-apt python3-git iptables ipset
      - apt update -y && apt install python-apt python3-apt python3-git iptables ipset
