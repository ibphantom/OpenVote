name: OpenVote
repository: ibphantom/openvote
network_mode: br0
webui: http://{{ip}}:{{port}}
ports:
  - "8000:8000/tcp"
