# Agent Instructions

## Running Tests

Before running tests, make sure the Python environment has the example project
dependencies installed.

Run the Django unit tests through the repository wrapper:

```sh
scripts/test
```

The wrapper changes into `example_project` before running:

```sh
python manage.py test
```

Do not run `python manage.py test` from the repository root.
