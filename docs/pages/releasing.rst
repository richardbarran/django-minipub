Releasing django-minipub
========================

Read the Docs builds documentation when a release tag is pushed to GitHub.
The tag gets its own documentation URL; ``/en/stable/`` follows the newest final
release and ``/en/latest/`` redirects to it. Documentation is validated locally
before release preparation; branch pushes and pull requests do not build it.

One-time Read the Docs setup
----------------------------

Complete this before pushing a release containing ``.readthedocs.yaml``:

* Keep the project's GitHub integration enabled. If using a repository webhook,
  keep it active; if using the RTD GitHub App, it receives events directly.
* Disable RTD pull-request builds. Remove any automation rules that activate
  or build branches or pull requests.
* Add an enabled automation rule with version type **Tag**, match **SemVer
  versions**, and action **Activate version**. This activates and builds release
  tags, including prereleases. RTD updates ``stable`` for final releases.
* Add an enabled rule with the same tag match and action **Trigger build for
  version**, without file or commit-message filters. Having this build rule
  prevents unmatched branch and pull-request events from triggering builds.
  Remove broader build rules that would also match those events.
* Keep ``stable`` active. Once a successful release build is available, select
  ``stable`` as the default version, then deactivate branch versions, including
  ``latest``.
* Configure an **Exact Redirect** from ``/en/latest/*`` to
  ``/en/stable/:splat``, so existing deep links retain their page paths.

No RTD API token or documentation environment is needed in GitHub Actions.
Remove any unused documentation publishing secret/environment left over from
an earlier setup.

See the official `automation rules
<https://docs.readthedocs.com/platform/stable/automation-rules.html>`_,
`Git integration
<https://docs.readthedocs.com/platform/stable/reference/git-integration.html>`_,
and `redirect documentation
<https://docs.readthedocs.com/platform/stable/user-defined-redirects.html>`_.
These are dashboard settings; ``.readthedocs.yaml`` configures how RTD builds
an individual version, not which GitHub events trigger builds. Automation rules
apply to new versions; activate existing release versions manually if needed.

Local validation
----------------

From the repository root::

    python -m pip install -e '.[dev,docs]'
    python -m sphinx -E -W --keep-going -b html docs docs/_build/html
    bin/test.py

Open ``docs/_build/html/index.html`` to inspect the output. Documentation builds
initialize Django using the example project's settings; no database is needed.
The prerelease hook uses this strict HTML build command. RTD also treats Sphinx
warnings as errors, using the configuration in the release tag.

Prepare and publish a release
-----------------------------

Start from a clean checkout of ``master`` with an updated changelog::

    uvx --from zest.releaser \
      --with-requirements release/requirements-release.txt \
      --with-editable '.[dev,docs]' \
      fullrelease

The prerelease hook builds documentation, runs Django tests, checks for missing
example migrations, and runs flake8. A failure stops release preparation.
Zest prepares local commits and a release tag, then advances the development
version. It does not push or upload packages.

Push the prepared commits and release tag. RTD receives the tag event, checks
out the tagged source, installs the documentation dependencies, runs Sphinx,
and publishes the documentation. Check the release and ``stable`` builds on
the `RTD builds page <https://app.readthedocs.org/projects/django-minipub/builds/>`_.

Run the separate PyPI workflow, for example for release ``1.12``::

    gh workflow run publish-pypi.yml --ref master -f release_tag=1.12

The postrelease hook attempts this dispatch if the tag is already on ``origin``;
otherwise it prints a recovery command. Pushing a tag does not itself dispatch
the PyPI workflow.

The two publications are independent: documentation can be available before the
package reaches PyPI, and a failed RTD build does not fail the PyPI workflow.
Check both before treating the release as complete or pushing the next release
tag. Prereleases get versioned documentation but do not move ``stable``.
The first release containing ``.readthedocs.yaml`` can use this configuration;
older tags may require separate compatibility work.

Recover documentation publication
---------------------------------

Inspect failures on the RTD builds page and use RTD's build controls to retry the
same release version and, if needed, ``stable``. A retry does not upload anything
to PyPI. Do not rerun a successful PyPI upload just because documentation failed.

If no build appeared, check the incoming integration event, automation rules,
and whether the version is active. If RTD disabled builds after repeated
failures, fix the cause and re-enable builds in the project settings.
If fixing the source or configuration inside a published tag is necessary,
prepare a new release instead of moving the existing tag.
