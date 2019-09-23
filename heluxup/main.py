"""
heluxup is able to parse the flux control repository for HelmReleases and checks if updates of the charts are
available. If updates are available heluxup updates the yaml files in the flux control respositroy accordingly.
"""

import os

import click
import semver
import urllib3
from ruamel.yaml import YAML

HTTP = urllib3.PoolManager()
YAML_PARSER = YAML()
YAML_PARSER.preserve_quotes = True
YAML_PARSER.width = 8000
REPO_CACHE = {}

class HelmRelease:
    """
    HelmRelease represents a HelmRelease object that is used by flux.
    """
    def __init__(self, release_name, chart_name, repository, git_version):
        self.release_name = release_name
        self.chart_name = chart_name
        self.repository = repository
        self.git_version = git_version

        if self.repository not in REPO_CACHE:
            repo_yaml = HTTP.request('GET', '{}/index.yaml'.format(self.repository))
            REPO_CACHE[self.repository] = YAML_PARSER.load(repo_yaml.data)

        self.available_versions = [version['version'] for
                                   version in REPO_CACHE[self.repository]['entries'][self.chart_name]]

        self.latest_version = self.available_versions[0]
        for version in self.available_versions[1:]:
            self.latest_version = version if semver.compare(self.latest_version.lstrip('v'),
                                                            version.lstrip('v')) < 0 else self.latest_version

    def __str__(self):
        return '{}: {} ({}) {}'.format(self.release_name, self.chart_name, self.git_version, self.repository)

    def __repr__(self):
        return self.__str__()


@click.command()
@click.option('--dry-run', '-d', is_flag=True, default=False, help='Print available updates without any modifications.')
@click.argument('git-directory', type=click.Path(exists=True, file_okay=False, dir_okay=True,
                                                 writable=True, readable=True))
def cli(dry_run, git_directory):
    """
    By using the flux helm operator (https://github.com/fluxcd/helm-operator-get-started) it is possible to manage
    helm charts in a git repository and flux takes care of the deployment.

    heluxup is able to parse the flux control repository for HelmReleases and checks if updates of the charts are
    available. If updates are available heluxup updates the yaml files in the flux control respositroy accordingly.
    (It is possible to pass --dry-run to check the changes without modifying any files.)

    GIT_DIRECTORY has to be an existing flux control repository.
    """
    dry_run_marker = '[dry-run] ' if dry_run else ''
    update_count = 0
    click.echo('{}Downloading all chart repository files can take a moment, please be patient.'
               .format(dry_run_marker))
    for root, _, files in os.walk(git_directory):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                path = os.path.join(root, file)
                with open(path, 'r') as file_read:
                    docs = list(YAML_PARSER.load_all(file_read))
                    for release in docs:
                        if release['kind'] == 'HelmRelease':
                            helm_release = HelmRelease(
                                release_name=release['spec']['releaseName'],
                                chart_name=release['spec']['chart']['name'],
                                repository=release['spec']['chart']['repository'],
                                git_version=release['spec']['chart']['version'],
                            )
                            if helm_release.git_version != helm_release.latest_version:
                                click.echo('{}Updating release {} ({}) from {} to {}'
                                           .format(dry_run_marker, helm_release.release_name, helm_release.chart_name,
                                                   helm_release.git_version, helm_release.latest_version))
                                update_count += 1
                                if not dry_run:
                                    release['spec']['chart']['version'] = helm_release.latest_version
                                    with open(path, 'w') as file_write:
                                        YAML_PARSER.dump_all(docs, file_write)
    click.echo('{}{} charts have been updated. \033[1mPlease verfiy the changes by running \'git diff\'\033[0m and make'
               ' sure to read upstream docs for major updates.'.format(dry_run_marker, update_count))
    click.echo('{}If you are sure about the changes commit them to your flux repository to apply them to your cluster.'
               .format(dry_run_marker))
