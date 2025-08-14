# -*- coding: utf-8 -*-

from which_bsm.impl import (
    get_aws_account_id_in_ci,
    BaseBotoSesEnum,
)

import pytest
import os


def create_base_boto_ses_enum(
    env_to_aws_profile_mapper=None,
    env_to_aws_region_mapper=None,
    default_app_env_name="dev",
    devops_env_name="devops",
    workload_role_name_prefix_in_ci="WorkloadRole-",
    workload_role_name_suffix_in_ci="-Role",
    is_local_runtime_group=True,
    is_ci_runtime_group=False,
) -> BaseBotoSesEnum:
    """Factory function to create BaseBotoSesEnum with sensible defaults."""
    if env_to_aws_profile_mapper is None:
        env_to_aws_profile_mapper = {"dev": "dev-profile", "prod": "prod-profile", "devops": "devops-profile"}
    
    if env_to_aws_region_mapper is None:
        env_to_aws_region_mapper = {"dev": "us-east-1", "prod": "us-west-2", "devops": "us-east-1"}
    
    return BaseBotoSesEnum(
        env_to_aws_profile_mapper=env_to_aws_profile_mapper,
        env_to_aws_region_mapper=env_to_aws_region_mapper,
        default_app_env_name=default_app_env_name,
        devops_env_name=devops_env_name,
        workload_role_name_prefix_in_ci=workload_role_name_prefix_in_ci,
        workload_role_name_suffix_in_ci=workload_role_name_suffix_in_ci,
        is_local_runtime_group=is_local_runtime_group,
        is_ci_runtime_group=is_ci_runtime_group,
        is_local=True,
        is_cloud9=False,
        is_ec2=False,
        is_lambda=False,
        is_batch=False,
        is_ecs=False,
        is_glue=False,
    )


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


class TestBaseBotoSesEnum:
    def test_get_workload_role_arn_in_ci(self):
        """Test get_workload_role_arn_in_ci method covering all logic branches."""

        # Create test instance using factory
        config = create_base_boto_ses_enum()

        # Test success case
        env_var_name = "DEV_AWS_ACCOUNT_ID"
        original_value = os.environ.get(env_var_name)

        try:
            os.environ[env_var_name] = "123456789012"
            arn = config.get_workload_role_arn_in_ci("dev")
            expected_arn = "arn:aws:iam::123456789012:role/WorkloadRole-dev-Role"
            assert arn == expected_arn

            # Test with different environment
            os.environ["PROD_AWS_ACCOUNT_ID"] = "987654321098"
            arn = config.get_workload_role_arn_in_ci("prod")
            expected_arn = "arn:aws:iam::987654321098:role/WorkloadRole-prod-Role"
            assert arn == expected_arn

            # Test devops environment rejection
            with pytest.raises(ValueError):
                config.get_workload_role_arn_in_ci("devops")

            # Test missing environment variable
            del os.environ[env_var_name]
            with pytest.raises(KeyError):
                config.get_workload_role_arn_in_ci("dev")

        finally:
            # Clean up
            for env_var in ["DEV_AWS_ACCOUNT_ID", "PROD_AWS_ACCOUNT_ID"]:
                if env_var in os.environ:
                    del os.environ[env_var]
            if original_value is not None:
                os.environ[env_var_name] = original_value

    def test_post_init_validation(self):
        """Test __post_init__ validation logic."""

        # Test valid configuration
        config = create_base_boto_ses_enum(
            workload_role_name_prefix_in_ci="Role-",
            workload_role_name_suffix_in_ci="-Suffix",
        )
        assert config.default_app_env_name == "dev"

        # Test invalid configuration - same env names
        with pytest.raises(ValueError):
            create_base_boto_ses_enum(
                default_app_env_name="devops",
                devops_env_name="devops",
            )

    def test_get_aws_profile_and_region(self):
        """Test get_aws_profile and get_aws_region methods."""
        
        config = create_base_boto_ses_enum()
        
        # Test successful profile retrieval
        assert config.get_aws_profile("dev") == "dev-profile"
        assert config.get_aws_profile("prod") == "prod-profile"
        
        # Test successful region retrieval  
        assert config.get_aws_region("dev") == "us-east-1"
        assert config.get_aws_region("prod") == "us-west-2"
        
        # Test missing environment in profile mapper
        with pytest.raises(KeyError):
            config.get_aws_profile("nonexistent")
            
        # Test missing environment in region mapper
        with pytest.raises(KeyError):
            config.get_aws_region("nonexistent")


if __name__ == "__main__":
    from which_bsm.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_bsm.impl",
        preview=False,
    )
