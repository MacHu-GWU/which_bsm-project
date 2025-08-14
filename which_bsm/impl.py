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
