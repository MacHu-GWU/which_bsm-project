# -*- coding: utf-8 -*-

"""
Define the boto session creation setup for this project.
"""

import dataclasses
from functools import cached_property

from boto_session_manager import BotoSesManager

from which_runtime.api import runtime
from which_env.api import BaseEnvNameEnum, CommonEnvNameEnum, detect_current_env
from which_bsm.api import BaseBotoSesEnum


class EnvNameEnum(BaseEnvNameEnum):
    devops = CommonEnvNameEnum.devops.value
    dev = CommonEnvNameEnum.dev.value
    tst = CommonEnvNameEnum.tst.value
    prd = CommonEnvNameEnum.prd.value


@dataclasses.dataclass
class BotoSesEnum(BaseBotoSesEnum):
    @cached_property
    def bsm_dev(self):
        return self.get_env_bsm(env_name=EnvNameEnum.dev.value)

    @cached_property
    def bsm_tst(self):
        return self.get_env_bsm(env_name=EnvNameEnum.tst.value)

    @cached_property
    def bsm_prd(self):
        return self.get_env_bsm(env_name=EnvNameEnum.prd.value)

    @cached_property
    def workload_bsm_list(self):
        return [
            self.bsm_dev,
            self.bsm_tst,
            self.bsm_prd,
        ]

    def print_who_am_i(self):  # pragma: no cover
        masked = not runtime.is_local_runtime_group
        for name, bsm in [
            ("bsm_devops", self.bsm_devops),
            ("bsm_dev", self.bsm_dev),
            ("bsm_tst", self.bsm_tst),
            ("bsm_prd", self.bsm_prd),
        ]:
            print(f"--- {name} ---")
            bsm.print_who_am_i(masked=masked)

    @cached_property
    def bsm(self) -> "BotoSesManager":
        current_env = detect_current_env(
            env_name_enum_class=EnvNameEnum,
            runtime=runtime,
        )
        return self.get_env_bsm(env_name=current_env)

    @classmethod
    def new(cls):
        return BotoSesEnum(
            env_to_aws_profile_mapper={
                EnvNameEnum.devops.value: "my_company_devops_us_east_1",
                EnvNameEnum.dev.value: "my_company_dev_us_east_1",
                EnvNameEnum.tst.value: "my_company_test_us_east_1",
                EnvNameEnum.prd.value: "my_company_prod_us_east_1",
            },
            env_to_aws_region_mapper={
                EnvNameEnum.devops.value: "us-east-1",
                EnvNameEnum.dev.value: "us-east-1",
                EnvNameEnum.tst.value: "us-east-1",
                EnvNameEnum.prd.value: "us-east-1",
            },
            default_app_env_name=EnvNameEnum.dev.value,
            devops_env_name=EnvNameEnum.devops.value,
            workload_role_name_prefix_in_ci="my_project_",
            workload_role_name_suffix_in_ci="_deployer",
            is_local_runtime_group=runtime.is_local_runtime_group,
            is_ci_runtime_group=runtime.is_ci_runtime_group,
            is_local=runtime.is_local,
            is_cloud9=runtime.is_aws_cloud9,
            is_ec2=runtime.is_aws_ec2,
            is_lambda=runtime.is_aws_lambda,
            is_batch=runtime.is_aws_batch,
            is_ecs=runtime.is_aws_ecs,
            is_glue=runtime.is_aws_glue,
        )


boto_ses_enum = BotoSesEnum.new()
