# -*- coding: utf-8 -*-

"""
See :class:`AbstractBotoSesFactory`.
"""

import typing as T
import os
import abc
import dataclasses
from pathlib import Path
from functools import cached_property

from boto_session_manager import BotoSesManager


def get_aws_account_id_in_ci(env_name: str) -> str:
    key = f"{env_name.upper()}_AWS_ACCOUNT_ID"
    try:
        value = os.environ[key]
    except KeyError:
        raise KeyError(
            f"Environment variable '{key}' is not set. "
            "Make sure to set it in your CI environment to store the AWS account ID."
        )
    if len(value) != 12:
        raise ValueError(
            f"Invalid AWS account ID '{value}' for environment '{env_name}'. "
            "It should be a 12-digit number."
        )
    if not value.isdigit():
        raise ValueError(
            f"Invalid AWS account ID '{value}' for environment '{env_name}'. "
            "It should contain only digits."
        )
    return value


@dataclasses.dataclass
class BaseBotoSesEnum(abc.ABC):
    """
    Base class for boto session factory enumeration.
    
    Provides configuration mapping between environments and AWS settings
    for managing boto sessions across different runtime contexts (local vs CI).
    Subclasses should implement environment-specific session creation logic.
    
    :param env_to_aws_profile_mapper: Mapping from environment names to AWS CLI profile names
    :param env_to_aws_region_mapper: Mapping from environment names to AWS regions
    :param default_app_env_name: Default application environment name
    :param devops_env_name: DevOps environment name (cannot be same as default_app_env_name)
    :param workload_role_name_prefix_in_ci: Prefix for workload IAM role names in CI
    :param workload_role_name_suffix_in_ci: Suffix for workload IAM role names in CI
    :param is_local_runtime_group: Whether this configuration is for local development
    :param is_ci_runtime_group: Whether this configuration is for CI environment
    
    Example:
        Configuration for multi-environment setup::
        
            {
                "env_to_aws_profile_mapper": {"dev": "my-dev-profile", "prod": "my-prod-profile"},
                "env_to_aws_region_mapper": {"dev": "us-east-1", "prod": "us-west-2"},
                "default_app_env_name": "dev",
                "devops_env_name": "devops",
                "workload_role_name_prefix_in_ci": "WorkloadRole-",
                "workload_role_name_suffix_in_ci": "-Role",
                "is_local_runtime_group": true,
                "is_ci_runtime_group": false
            }
    
    .. note::
        The devops_env_name must be different from default_app_env_name to maintain
        proper separation between application and operations environments.
    """

    env_to_aws_profile_mapper: dict[str, str] = dataclasses.field()
    env_to_aws_region_mapper: dict[str, str] = dataclasses.field()
    default_app_env_name: str = dataclasses.field()
    devops_env_name: str = dataclasses.field()
    workload_role_name_prefix_in_ci: str = dataclasses.field()
    workload_role_name_suffix_in_ci: str = dataclasses.field()
    is_local_runtime_group: bool = dataclasses.field()
    is_ci_runtime_group: bool = dataclasses.field()

    def __post_init__(self):
        if self.default_app_env_name == self.devops_env_name:
            raise ValueError(
                f"default_app_env_name cannot be devops_env_name! "
                f"'{self.devops_env_name}' is NOT an app environment."
            )

    def get_workload_role_arn_in_ci(self, env_name: str) -> str:
        """
        Generate the workload IAM role ARN for the specified environment in CI.
        
        Constructs the full ARN for the workload role that should be assumed
        in CI environments for deployment operations. The role name is built
        using the configured prefix, environment name, and suffix.
        
        :param env_name: Target environment name for the workload role
        
        :returns: Complete IAM role ARN for the workload environment
        
        :raises ValueError: If env_name is the devops environment
        :raises KeyError: If AWS account ID environment variable is not set
        
        .. note::
            This method is primarily used in CI environments where AWS CLI
            profiles are not available. In local development, use AWS CLI
            named profiles instead.
        """
        if env_name == self.devops_env_name:
            raise ValueError(
                f"You cannot use the devops environment '{self.devops_env_name}' "
                f"to get workload role ARN in CI."
            )
        aws_account_id = os.environ[f"{env_name.upper()}_AWS_ACCOUNT_ID"]
        return (
            f"arn:aws:iam::{aws_account_id}:role/"
            f"{self.workload_role_name_prefix_in_ci}{env_name}{self.workload_role_name_suffix_in_ci}"
        )

    def get_workfload_role_session_name(self, env_name: str) -> str:  # pragma: no cover
        """
        Generate a session name for the workload role assumption.
        
        Creates a standardized session name format for role assumption operations.
        This helps with tracking and auditing role usage in AWS CloudTrail.
        
        :param env_name: Environment name to include in the session name
        
        :returns: Formatted session name for role assumption
        """
        return f"{env_name}_role_session"
