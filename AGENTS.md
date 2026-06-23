# Agent Instructions

## Running Tests

Before running tests, make sure the Python environment has the example project
dependencies installed.

Run the Django unit tests through the repository wrapper:

```sh
scripts/test.sh
```

The wrapper changes into `example_project` before running:

```sh
python manage.py test
```

Do not run `python manage.py test` from the repository root.

## Running the Tox Matrix

To run the full Python/Django test matrix, use tox from the repository root:

```sh
tox
```

This requires tox and the configured Python interpreters to be available in the
active Python environment.
