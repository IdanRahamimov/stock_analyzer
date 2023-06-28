import unittest.mock
import json
import os
import io
from app.main import load_config



def test_load_config():
    # Mock configuration (not a real key)
    config ={"KEY": "GERE8589SF93FD"}

    # Mock os.path.exists to always return True
    with unittest.mock.patch.object(os.path, 'exists', eturn_value=True):
        # Mock open function
        with unittest.mock.patch('builtins.open', return_value=io.StringIO(json.dumps(config))):
            # Check that the returned dictionary matches the expected configuration
            result = load_config()

    # Check that the returned dictionary matches the expected configuration
    assert result == config

    # Check that all expected keys are in the configuration and their values are not empty
    for key in ['KEY']:
        assert key in result and result[key] != ""