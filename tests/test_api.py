# -*- coding: utf-8 -*-

from which_bsm import api


def test():
    _ = api


if __name__ == "__main__":
    from which_bsm.tests import run_cov_test

    run_cov_test(
        __file__,
        "which_bsm.api",
        preview=False,
    )
