# -*- coding: utf-8 -*-

from which_bsm.impl import get_aws_account_id_in_ci

import pytest
import os


def test_get_aws_account_id_in_ci():
    """Test get_aws_account_id_in_ci function covering all logic branches."""
    
    env_name = "TEST"
    env_var_name = f"{env_name.upper()}_AWS_ACCOUNT_ID"
    original_value = os.environ.get(env_var_name)
    
    try:
        # Success case
        os.environ[env_var_name] = "123456789012"
        assert get_aws_account_id_in_ci(env_name) == "123456789012"
        
        # Environment variable not set
        del os.environ[env_var_name]
        with pytest.raises(KeyError):
            get_aws_account_id_in_ci(env_name)
        
        # Wrong length - too short
        os.environ[env_var_name] = "12345"
        with pytest.raises(ValueError):
            get_aws_account_id_in_ci(env_name)
        
        # Wrong length - too long
        os.environ[env_var_name] = "1234567890123"
        with pytest.raises(ValueError):
            get_aws_account_id_in_ci(env_name)
        
        # Non-digit characters
        os.environ[env_var_name] = "12345678901a"
        with pytest.raises(ValueError):
            get_aws_account_id_in_ci(env_name)
        
        # Letters only
        os.environ[env_var_name] = "abcdefghijkl"
        with pytest.raises(ValueError):
            get_aws_account_id_in_ci(env_name)
        
        # Mixed case environment name
        os.environ["DEV_AWS_ACCOUNT_ID"] = "123456789012"
        assert get_aws_account_id_in_ci("dev") == "123456789012"
        del os.environ["DEV_AWS_ACCOUNT_ID"]
        
    finally:
        # Clean up
        if env_var_name in os.environ:
            del os.environ[env_var_name]
        if original_value is not None:
            os.environ[env_var_name] = original_value


if __name__ == "__main__":
    from which_bsm.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_bsm.impl",
        preview=False,
    )
