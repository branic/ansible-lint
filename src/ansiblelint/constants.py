"""Constants used by AnsibleLint."""

from enum import Enum
from pathlib import Path
from typing import Literal

DEFAULT_RULESDIR = Path(__file__).parent / "rules"
CUSTOM_RULESDIR_ENVVAR = "ANSIBLE_LINT_CUSTOM_RULESDIR"
RULE_DOC_URL = "https://ansible.readthedocs.io/projects/lint/rules/"
SKIP_SCHEMA_UPDATE = "ANSIBLE_LINT_SKIP_SCHEMA_UPDATE"

ENV_VARS_HELP = {
    CUSTOM_RULESDIR_ENVVAR: "Used for adding another folder into the lookup path for new rules.",
    "ANSIBLE_LINT_IGNORE_FILE": "Define it to override the name of the default ignore file `.ansible-lint-ignore`",
    "ANSIBLE_LINT_WRITE_TMP": "Tells linter to dump fixes into different temp files instead of overriding original. Used internally for testing.",
    SKIP_SCHEMA_UPDATE: "Tells ansible-lint to skip schema refresh.",
    "ANSIBLE_LINT_NODEPS": "Avoids installing content dependencies and avoids performing checks that would fail when modules are not installed. Far less violations will be reported.",
}

EPILOG = (
    "The following environment variables are also recognized but there is no guarantee that they will work in future versions:\n\n"
    + "\n".join(f"{key}: {value}\n" for key, value in ENV_VARS_HELP.items())
)


# Not using an IntEnum because only starting with py3.11 it will evaluate it
# as int.
class RC:  # pylint: disable=too-few-public-methods
    """All exit codes used by ansible-lint."""

    SUCCESS = 0
    VIOLATIONS_FOUND = 2
    INVALID_CONFIG = 3
    LOCK_TIMEOUT = 4
    NO_FILES_MATCHED = 5
    EXIT_CONTROL_C = 130


ANSIBLE_MOCKED_MODULE = """\
# This is a mocked Ansible module generated by ansible-lint
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
module: {name}

short_description: Mocked
version_added: "1.0.0"
description: Mocked

author:
    - ansible-lint (@nobody)
'''
EXAMPLES = '''mocked'''
RETURN = '''mocked'''


def main():
    result = dict(
        changed=False,
        original_message='',
        message='')

    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )
    module.exit_json(**result)


if __name__ == "__main__":
    main()
"""

FileType = Literal[
    "playbook",
    "rulebook",
    "meta",  # role meta
    "meta-runtime",
    "tasks",  # includes pre_tasks, post_tasks
    "handlers",  # very similar to tasks but with some specifics
    # https://docs.ansible.com/ansible/latest/galaxy/user_guide.html#installing-roles-and-collections-from-the-same-requirements-yml-file
    "requirements",
    "role",  # that is a folder!
    "yaml",  # generic yaml file, previously reported as unknown file type
    "ansible-lint-config",
    "sanity-ignore-file",  # tests/sanity/ignore file
    "plugin",
    "",  # unknown file type
]


# Aliases for deprecated tags/ids and their newer names
RENAMED_TAGS = {
    "102": "no-jinja-when",
    "104": "deprecated-bare-vars",
    "105": "deprecated-module",
    "106": "role-name",
    "202": "risky-octal",
    "203": "no-tabs",
    "205": "playbook-extension",
    "206": "jinja[spacing]",
    "207": "jinja[invalid]",
    "208": "risky-file-permissions",
    "301": "no-changed-when",
    "302": "deprecated-command-syntax",
    "303": "command-instead-of-module",
    "304": "inline-env-var",
    "305": "command-instead-of-shell",
    "306": "risky-shell-pipe",
    "401": "latest[git]",
    "402": "latest[hg]",
    "403": "package-latest",
    "404": "no-relative-paths",
    "501": "partial-become",
    "502": "name[missing]",
    "503": "no-handler",
    "504": "deprecated-local-action",
    "505": "missing-import",
    "601": "literal-compare",
    "602": "empty-string-compare",
    "702": "meta-no-tags",
    "703": "meta-incorrect",
    "704": "meta-video-links",
    "911": "syntax-check",
    "deprecated-command-syntax": "no-free-form",
    "fqcn-builtins": "fqcn[action-core]",
    "git-latest": "latest[git]",
    "hg-latest": "latest[hg]",
    "no-jinja-nesting": "jinja[invalid]",
    "no-loop-var-prefix": "loop-var-prefix",
    "unnamed-task": "name[missing]",
    "var-spacing": "jinja[spacing]",
}

PLAYBOOK_TASK_KEYWORDS = [
    "tasks",
    "handlers",
    "pre_tasks",
    "post_tasks",
]
PLAYBOOK_ROLE_KEYWORDS = [
    "any_errors_fatal",
    "become",
    "become_exe",
    "become_flags",
    "become_method",
    "become_user",
    "check_mode",
    "collections",
    "connection",
    "debugger",
    "delegate_facts",
    "delegate_to",
    "diff",
    "environment",
    "ignore_errors",
    "ignore_unreachable",
    "module_defaults",
    "name",
    "role",
    "no_log",
    "port",
    "remote_user",
    "run_once",
    "tags",
    "throttle",
    "timeout",
    "vars",
    "when",
]
NESTED_TASK_KEYS = [
    "block",
    "always",
    "rescue",
]

# Keys that are used internally when parsing YAML/JSON files
SKIPPED_RULES_KEY = "__skipped_rules__"
LINE_NUMBER_KEY = "__line__"
FILENAME_KEY = "__file__"
ANNOTATION_KEYS = [
    FILENAME_KEY,
    LINE_NUMBER_KEY,
    SKIPPED_RULES_KEY,
    "__ansible_module__",
    "__ansible_module_original__",
]
INCLUSION_ACTION_NAMES = {
    "include",
    "include_tasks",
    "import_playbook",
    "import_tasks",
    "ansible.builtin.include",
    "ansible.builtin.include_tasks",
    "ansible.builtin.import_playbook",
    "ansible.builtin.import_tasks",
}

ROLE_IMPORT_ACTION_NAMES = {
    "ansible.builtin.import_role",
    "ansible.builtin.include_role",
    "ansible.legacy.import_role",
    "ansible.legacy.include_role",
    "import_role",
    "include_role",
}

CONFIG_FILENAMES = [
    ".ansible-lint",
    ".ansible-lint.yml",
    ".ansible-lint.yaml",
    ".config/ansible-lint.yml",
    ".config/ansible-lint.yaml",
]


class States(Enum):
    """States used are used as sentinel values in various places."""

    NOT_LOADED = "File not loaded"
    LOAD_FAILED = "File failed to load"
    UNKNOWN_DATA = "Unknown data"

    def __bool__(self) -> bool:
        """Ensure all states evaluate as False as booleans."""
        return False
