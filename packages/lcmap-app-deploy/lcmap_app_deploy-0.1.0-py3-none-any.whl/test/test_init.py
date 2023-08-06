"""
Unit tests for app_deploy.__init__.py
"""
import re
import app_deploy


def test_version():
    """Validate semantic version string."""
    version = app_deploy.version()
    print(f"> version is: {version}")

    pattern = r"[0-9]+\.[0-9]+\.[0-9]+"
    assert re.search(pattern, version)
