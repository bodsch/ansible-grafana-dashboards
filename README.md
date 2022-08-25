# Ansible Role:  `grafana_dashboards`

Importer for varoius Grafana Dashboards

Supports folder for an better structure.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-grafana-dashboards/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-grafana-dashboards)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-grafana-dashboards)][releases]

[ci]: https://github.com/bodsch/ansible-grafana-dashboards/actions
[issues]: https://github.com/bodsch/ansible-grafana-dashboards/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-grafana-dashboards/releases


## Requirements & Dependencies



### Operating systems

Tested on

* Arch Linux
* Artix Linux
* Debian based
    - Debian 11

## configuration

```yaml
grafana_dashboards_upgrade: false

grafana_dashboards_git:
  update: true
  url: ""
  version: ""

# vars from grafana role
grafana_provisioning_synced: false
grafana_data_dir: /var/lib/grafana
```

---

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-grafana-dashboards/-/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

`FREE SOFTWARE, HELL YEAH!`
