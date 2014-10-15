import subprocess


def prereleaser_middle(data):
    """
    1. Run the unit tests one last time before we make a release.
    2. Check that code follows PEP8 conventions (more or less).
    """
    print('Running unit tests.')
    subprocess.check_output(["python", "example_project/manage.py", "test", "news", "news_with_archive"])

    print('Running PEP8 check.')
    # See setup.cfg for configuration options.
    subprocess.check_output(["pep8"])
