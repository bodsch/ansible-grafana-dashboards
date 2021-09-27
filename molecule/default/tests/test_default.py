
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar
import pytest
import os
import testinfra.utils.ansible_runner

import pprint
pp = pprint.PrettyPrinter()

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def base_directory():
    cwd = os.getcwd()

    if('group_vars' in os.listdir(cwd)):
        directory = "../.."
        molecule_directory = "."
    else:
        directory = "."
        molecule_directory = "molecule/{}".format(os.environ.get('MOLECULE_SCENARIO_NAME'))

    return directory, molecule_directory


@pytest.fixture()
def get_vars(host):
    """

    """
    base_dir, molecule_dir = base_directory()

    file_defaults = "file={}/defaults/main.yml name=role_defaults".format(base_dir)
    file_vars = "file={}/vars/main.yml name=role_vars".format(base_dir)
    file_molecule = "file={}/group_vars/all/vars.yml name=test_vars".format(molecule_dir)

    defaults_vars = host.ansible("include_vars", file_defaults).get("ansible_facts").get("role_defaults")
    vars_vars = host.ansible("include_vars", file_vars).get("ansible_facts").get("role_vars")
    molecule_vars = host.ansible("include_vars", file_molecule).get("ansible_facts").get("test_vars")

    ansible_vars = defaults_vars
    ansible_vars.update(vars_vars)
    ansible_vars.update(molecule_vars)

    templar = Templar(loader=DataLoader(), variables=ansible_vars)
    result = templar.template(ansible_vars, fail_on_undefined=False)

    return result


@pytest.mark.parametrize("dirs", [
    "/var/lib/grafana/dashboards/backend",
    "/var/lib/grafana/dashboards/frontend",
    "/var/lib/grafana/dashboards/delivery",
    "/var/lib/grafana/dashboards/licenses",
    "/var/lib/grafana/dashboards/databases",
    "/var/lib/grafana/dashboards/overviews",
])
def test_directories(host, dirs):
    d = host.file(dirs)
    assert d.is_directory
    assert d.group == "grafana"
    assert d.mode == 0o755


@pytest.mark.parametrize("files", [
    "/etc/grafana/provisioning/dashboards/backend.yml",
    "/etc/grafana/provisioning/dashboards/frontend.yml",
    "/etc/grafana/provisioning/dashboards/delivery.yml",
    "/etc/grafana/provisioning/dashboards/licenses.yml",
    "/etc/grafana/provisioning/dashboards/databases.yml",
    "/etc/grafana/provisioning/dashboards/overviews.yml",
])
def test_files(host, files):
    f = host.file(files)
    assert f.is_file
    assert f.group == "grafana"
    assert f.mode == 0o640
