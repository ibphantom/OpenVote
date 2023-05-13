name: OpenVote
repository: yourusername/openvote
network_mode: bridge
webui: http://{{ip}}:{{port}}
ports:
  - "8000:8000/tcp"
