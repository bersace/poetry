from typing import Union

from poetry.semver.helpers import parse_stability
from poetry.semver.version_parser import VersionParser

from .dependency import Dependency
from .vcs_dependency import VCSDependency


class Package:

    supported_link_types = {
        'require': {
            'description': 'requires',
            'method': 'requires'
        },
        'provide': {
            'description': 'provides',
            'method': 'provides'
        }
    }

    STABILITY_STABLE = 0
    STABILITY_RC = 5
    STABILITY_BETA = 10
    STABILITY_ALPHA = 15
    STABILITY_DEV = 20

    stabilities = {
        'stable': STABILITY_STABLE,
        'rc': STABILITY_RC,
        'beta': STABILITY_BETA,
        'alpha': STABILITY_ALPHA,
        'dev': STABILITY_DEV,
    }

    def __init__(self, name, version, pretty_version=None):
        """
        Creates a new in memory package.
        """
        self._pretty_name = name
        self._name = name.lower()

        self._version = version
        self._pretty_version = pretty_version or version

        self.description = ''

        self._stability = parse_stability(version)
        self._dev = self._stability == 'dev'

        self._authors = []

        self.homepage = None
        self.repository_url = None
        self.keywords = []
        self.license = None
        self.readme = ''

        self.source_type = ''
        self.source_reference = ''
        self.source_url = ''

        self.requires = []
        self.dev_requires = []
        self.extras = {}

        self._parser = VersionParser()

        self.category = 'main'
        self.hashes = []
        self.optional = False

        # Requirements for making it mandatory
        self.requirements = {}

        self._python_versions = '*'
        self._python_constraint = self._parser.parse_constraints('*')
        self._platform = '*'
        self._platform_constraint = self._parser.parse_constraints('*')

    @property
    def name(self):
        return self._name

    @property
    def pretty_name(self):
        return self._pretty_name

    @property
    def version(self):
        return self._version

    @property
    def pretty_version(self):
        return self._pretty_version

    @property
    def unique_name(self):
        return self.name + '-' + self._version

    @property
    def pretty_string(self):
        return self.pretty_name + ' ' + self.pretty_version
    
    @property
    def full_pretty_version(self):
        if not self._dev and self.source_type not in ['hg', 'git']:
            return self._pretty_version

        # if source reference is a sha1 hash -- truncate
        if len(self.source_reference) == 40:
            return '{} {}'.format(self._pretty_version,
                                  self.source_reference[0:7])

        return '{} {}'.format(self._pretty_version, self.source_reference)

    @property
    def authors(self) -> list:
        return self._authors

    @property
    def python_versions(self):
        return self._python_versions

    @python_versions.setter
    def python_versions(self, value: str):
        self._python_versions = value
        self._python_constraint = self._parser.parse_constraints(value)

    @property
    def python_constraint(self):
        return self._python_constraint

    @property
    def platform(self) -> str:
        return self._platform

    @platform.setter
    def platform(self, value: str):
        self._platform = value
        self._platform_constraint = self._parser.parse_constraints(value)

    @property
    def platform_constraint(self):
        return self._platform_constraint

    def is_dev(self):
        return self._dev

    def is_prerelease(self):
        return self._stability != 'stable'

    def add_dependency(self,
                       name: str,
                       constraint: Union[str, dict, None] = None,
                       category: str = 'main') -> Dependency:
        if constraint is None:
            constraint = '*'

        if isinstance(constraint, dict):
            if 'git' in constraint:
                # VCS dependency
                optional = constraint.get('optional', False)
                python_versions = constraint.get('python')
                platform = constraint.get('platform')

                dependency = VCSDependency(
                    name,
                    'git', constraint['git'],
                    branch=constraint.get('branch', None),
                    tag=constraint.get('tag', None),
                    rev=constraint.get('rev', None),
                    optional=optional,
                )

                if python_versions:
                    dependency.python_versions = python_versions

                if platform:
                    dependency.platform = platform
            else:
                version = constraint['version']
                optional = constraint.get('optional', False)
                allows_prereleases = constraint.get('allows_prereleases', False)
                python_versions = constraint.get('python')
                platform = constraint.get('platform')

                dependency = Dependency(
                    name, version,
                    optional=optional,
                    category=category,
                    allows_prereleases=allows_prereleases
                )

                if python_versions:
                    dependency.python_versions = python_versions

                if platform:
                    dependency.platform = platform

            if 'extras' in constraint:
                for extra in constraint['extras']:
                    dependency.extras.append(extra)
        else:
            dependency = Dependency(name, constraint, category=category)

        if category == 'dev':
            self.dev_requires.append(dependency)
        else:
            self.requires.append(dependency)

        return dependency

    def __hash__(self):
        return hash((self._name, self._version))

    def __eq__(self, other):
        if not isinstance(other, Package):
            return NotImplemented

        return self._name == other.name and self._version == other.version

    def __str__(self):
        return self.unique_name

    def __repr__(self):
        return '<Package {}>'.format(self.unique_name)
