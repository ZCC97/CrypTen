#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from crypten.common import constants
from crypten.common.rng import generate_kbit_random_tensor, generate_random_ring_element


def share(secret, num_parties=2):
    """Create an arithmetic (additive) sharing from a secret"""
    # For single process, do not encrypt (for debugging purposes)
    if num_parties < 2:
        return secret

    shares0 = generate_random_ring_element(secret.size())
    shares1 = secret - shares0
    if num_parties == 2:
        return shares0, shares1
    return (shares0, *share(shares1, num_parties=(num_parties - 1)))


def xor_share(secret, bitlength=constants.BITS, num_parties=2):
    """Create a boolean (xor) sharing from a secret"""
    # For single process, do not encrypt (for debugging purposes)
    if num_parties < 2:
        return secret

    shares0 = generate_kbit_random_tensor(secret.size(), bitlength=bitlength)
    shares1 = secret ^ shares0
    if num_parties == 2:
        return shares0, shares1
    return (
        shares0,
        *xor_share(shares1, bitlength=constants.BITS, num_parties=(num_parties - 1)),
    )
