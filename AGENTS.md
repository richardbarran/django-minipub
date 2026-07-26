# Agent Instructions

## Updating Django and Python Compatibility

Use this runbook when updating the project for supported Django and Python
releases:

1. Check supported Django releases, their Python compatibility, and maintained
   Python versions using the official Django and Python documentation.
2. Build the target matrix from supported combinations, excluding prereleases
   unless they were explicitly requested.
3. Run `scripts/test.py` and `tox` before making compatibility changes.
4. Re-run `scripts/test.py` with `PYTHONWARNINGS=default` and resolve
   project-owned deprecation warnings.
5. Keep `tox.ini`, `pyproject.toml` classifiers, and
   `.github/workflows/ci.yml` consistent with the target matrix.
6. Review and test dependency lower bounds across `requirements.txt`,
   `dev-requirements.txt`, and `example_project/requirements.txt`.
7. Update the current unreleased section of `CHANGELOG.txt`, then re-run the
   complete tox matrix.

If target interpreters are unavailable locally, continue with configuration
updates from official sources and report that complete verification depends on
CI.

## Updating the Changelog

When a change affects users, compatibility, migrations, dependencies, packaging,
or release behavior, add a concise entry under the current unreleased section
of `CHANGELOG.txt`. Remove `- Nothing changed yet.` when adding the first entry.
For pull-request changes, end the entry with the pull request number, for
example `- Added support for a new Django version. (#123)`.

## Preparing a Pull Request

Before finalizing a pull request, review its changes and ensure all required
changelog entries are present. If the wording or need for an entry is unclear,
propose it before finalizing the pull request.

## Running Tests

Before running tests, make sure the Python environment has the example project
dependencies installed.

Run the Django unit tests through the repository wrapper:

```sh
scripts/test.py
```

The wrapper changes into `example_project` before running:

```sh
python3 manage.py test
```

Do not run `python manage.py test` from the repository root.

## Running the Tox Matrix

To run the full Python/Django test matrix, use tox from the repository root:

```sh
tox
```

This requires tox and the configured Python interpreters to be available in the
active Python environment.
