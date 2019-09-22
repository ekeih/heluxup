# heluxup

By using the [flux helm operator](https://github.com/fluxcd/helm-operator-get-started) it is possible to manage
helm charts in a git repository and `flux` takes care of the deployment.

`heluxup` is able to parse the flux control repository for HelmReleases and checks if updates of the charts are
available. If updates are available `heluxup` updates the yaml files in the flux control respositroy accordingly.
(It is possible to pass `--dry-run` to check the changes without modifying any files.)

## Installation

Simply install `heluxup` with [pip](https://pypi.org/project/heluxup/)

```bash
$ pip install heluxup
```

or clone the repository

```bash
$ git clone git@github.com:ekeih/heluxup.git
$ cd heluxup
$ pip install -e .
```

## Usage

```
$ heluxup /home/max/repos/flux-control/
Downloading all chart repository files can take a moment, please be patient.
Updating release ingress-controller (nginx-ingress) from 1.17.1 to 1.21.0
Updating release oauth2 (oauth2-proxy) from 0.14.0 to 0.14.1
Updating release cert-manager (cert-manager) from v0.9.1 to v0.10.0
Updating release omnbot-influxdb (influxdb) from 1.3.2 to 1.4.0
Updating release omnbot-redis (redis) from 9.1.2 to 9.1.12
Updating release prom (prometheus-operator) from 6.7.3 to 6.11.0
Updating release blackbox-exporter (prometheus-blackbox-exporter) from 1.1.0 to 1.3.0
Updating release kubewatch (kubewatch) from 0.8.5 to 0.8.9
Updating release loki (loki-stack) from 0.16.0 to 0.16.2
Updating release postgresql-production (postgresql) from 6.3.2 to 6.3.9
Updating release postgresql-development (postgresql) from 6.3.2 to 6.3.9
11 charts have been updated. Please verfiy the changes by running 'git diff' and make sure to read upstream docs for major updates.
If you are sure about the changes commit them to your flux repository to apply them to your cluster.
```

It is also possible to execute a dry-run which shows available updates without any modifications to the control repository.

```
$ heluxup -d /home/max/repos/flux-control/
[dry-run] Downloading all chart repository files can take a moment, please be patient.
[dry-run] Updating release ingress-controller (nginx-ingress) from 1.17.1 to 1.21.0
[dry-run] Updating release oauth2 (oauth2-proxy) from 0.14.0 to 0.14.1
[dry-run] Updating release cert-manager (cert-manager) from v0.9.1 to v0.10.0
[dry-run] Updating release omnbot-influxdb (influxdb) from 1.3.2 to 1.4.0
[dry-run] Updating release omnbot-redis (redis) from 9.1.2 to 9.1.12
[dry-run] Updating release prom (prometheus-operator) from 6.7.3 to 6.11.0
[dry-run] Updating release blackbox-exporter (prometheus-blackbox-exporter) from 1.1.0 to 1.3.0
[dry-run] Updating release kubewatch (kubewatch) from 0.8.5 to 0.8.9
[dry-run] Updating release loki (loki-stack) from 0.16.0 to 0.16.2
[dry-run] Updating release postgresql-production (postgresql) from 6.3.2 to 6.3.9
[dry-run] Updating release postgresql-development (postgresql) from 6.3.2 to 6.3.9
[dry-run] 11 charts have been updated. Please verfiy the changes by running 'git diff' and make sure to read upstream docs for major updates.
[dry-run] If you are sure about the changes commit them to your flux repository to apply them to your cluster.
```

## License

```
heluxup makes it easy to upgrade HelmRelease objects in a flux control respository.
Copyright (C) 2019  Max Rosin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```