import sys

import yaml

# README:
# conda activate q2dev
#
# This script takes two positional arguments:
# argv[1]: a busywork filepath with yaml package listing
# argv[2]: a filepath to write a txt of package names to


def read_packages(variables_fp):
    with open(variables_fp) as fh:
        variables = yaml.load(fh)
    return [v['name'] for v in variables['projects']]


def write_packages(packages_fp, packages):
    with open(packages_fp, 'w') as fh:
        for package in packages:
            fh.write('%s\n' % (package,))


if __name__ == '__main__':
    variables_fp = sys.argv[1]
    packages = read_packages(variables_fp)

    packages_fp = sys.argv[2]
    write_packages(packages_fp, packages)
