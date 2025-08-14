# -*- coding: utf-8 -*-

from which_bsm import api


def test():
    _ = api
    _ = api.get_aws_account_id_in_ci
    _ = api.BaseBotoSesEnum


if __name__ == "__main__":
    from which_bsm.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_bsm.api",
        preview=False,
    )
