# Fleet-watch

Fleet Watch monitors the health of a fleet of Linux servers. An agent runs on each host, collects health data, and reports it. Over time this grows into a cloud service: a Python agent reporting to a REST API, containerized, deployed to AWS with Terraform, and shipped through CI/CD.

# Repository layout

fleet-watch/
├── agent/
│   └── healthcheck.sh       # health-check agent
├── deploy/
│   ├── fleetwatch.service   # systemd unit that runs one check
│   ├── fleetwatch.timer     # runs the service every 5 minutes
│   └── fleetwatch.logrotate # daily rotation, keeps 7 days
└── README.md


# Requirements

A Linux host with systemd 
Bash 4+
shellcheck (development only)
jq (optional, only for checking JSON output)

# Exit codes
Code	Meaning
0	All checks OK
1	At least one WARN
2	At least one CRIT

CRIT rules:

Any disk over 95% used
Any listed service not active
TODO: the other CRIT rules you chose, and why


Notes :
