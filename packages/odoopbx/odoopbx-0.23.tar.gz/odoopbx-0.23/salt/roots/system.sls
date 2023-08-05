system-python-apt:
  cmd.run:
    - name: apt install python3-apt
    - unless: dpkg -l python3-apt
