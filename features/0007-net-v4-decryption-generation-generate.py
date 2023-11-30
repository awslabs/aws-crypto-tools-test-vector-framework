# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
#
# Only Python 3.7+ compatibility is guaranteed.

import argparse
import json
import os
import sys
import uuid
from urllib.parse import urlunparse

from awses_message_encryption_utils import (
    ALGORITHM_SUITES,
    EMPTY_ENCRYPTION_CONTEXT,
    PLAINTEXTS,
    _providers,
    NON_UNICODE_ENCRYPTION_CONTEXT, DEFAULT_CMM, REQUIRED_CMM, ALGORITHM_SUITES_COMMITTING,
    ALGORITHM_SUITES_NO_KDF,
)

MANIFEST_VERSION = 4


def _test_name(algorithm, ec: dict[str, str], cmm) -> str:
    return f"{algorithm}-ec_len_{len(ec)}-cmm_{cmm}-{str(uuid.uuid4())}"


def _build_tests_valid_net_4_0_0(keys):
    """
    The ESDK-NET v4.0.0 produced valid messages
    under BOTH these conditions:
    - Required Encryption Context CMM
    - No KDF or Yes Key Commitment

     The Keyring/Master Key Provider is relevant,
     only the CMM's treatment of Encryption Context
     and the algorithm suite.
    :param dict keys: Parsed keys manifest
    """
    frame_size = 512
    plaintext = "small"
    suites_that_worked_with_required = ALGORITHM_SUITES_COMMITTING + ALGORITHM_SUITES_NO_KDF
    for cmm in [REQUIRED_CMM]:
        for ec in [NON_UNICODE_ENCRYPTION_CONTEXT]:
            for algorithm in suites_that_worked_with_required:
                for provider_set in _providers(keys):
                    yield (
                        _test_name(algorithm, ec, cmm),
                        {
                            "encryption-scenario": {
                                "plaintext": plaintext,
                                "algorithm": algorithm,
                                "frame-size": frame_size,
                                "encryption-context": ec,
                                "master-keys": provider_set,
                                "cmm": cmm
                            }
                        },
                    )


def _build_tests_invalid_net_4_0_0(keys):
    """
    The ESDK-NET v4.0.0 produced invalid messages
    under all conditions other than those described
    in _build_tests_valid_net_4_0_0.

    The Keyring/Master Key Provider is irrelevant,
    only the CMM's treatment of Encryption Context
    and the algorithm suite.
    :param dict keys: Parsed keys manifest
    """
    suites_that_worked_with_required = ALGORITHM_SUITES_COMMITTING + ALGORITHM_SUITES_NO_KDF
    suites_that_did_not_work_with_required = list(
        filter(lambda _alg: _alg not in suites_that_worked_with_required, ALGORITHM_SUITES)
    )
    frame_size = 512
    plaintext = "small"
    for cmm in [REQUIRED_CMM]:
        for ec in [NON_UNICODE_ENCRYPTION_CONTEXT]:
            for algorithm in suites_that_did_not_work_with_required:
                for provider_set in _providers(keys):
                    yield (
                        _test_name(algorithm, ec, cmm),
                        {
                            "encryption-scenario": {
                                "plaintext": plaintext,
                                "algorithm": algorithm,
                                "frame-size": frame_size,
                                "encryption-context": ec,
                                "master-keys": provider_set,
                                "cmm": cmm
                            }
                        },
                    )
    for cmm in [DEFAULT_CMM]:
        for ec in [NON_UNICODE_ENCRYPTION_CONTEXT, EMPTY_ENCRYPTION_CONTEXT]:
            for algorithm in ALGORITHM_SUITES:
                for provider_set in _providers(keys):
                    yield (
                        _test_name(algorithm, ec, cmm),
                        {
                            "encryption-scenario": {
                                "plaintext": plaintext,
                                "algorithm": algorithm,
                                "frame-size": frame_size,
                                "encryption-context": ec,
                                "master-keys": provider_set,
                                "cmm": cmm
                            }
                        },
                    )


def build_manifest(keys_filename: str, valid: bool):
    """Build the test-case manifest which directs
    the behavior of cross-compatibility clients.

    :param str keys_filename: Name of file containing the keys manifest
    :param bool valid: Generate Valid or Invalid ESDK-NET v4.0.0 messages
    """
    with open(keys_filename, "r") as keys_file:
        keys = json.load(keys_file)

    keys_path = "/".join(keys_filename.split(os.path.sep))
    keys_uri = urlunparse(("file", keys_path, "", "", "", ""))
    tests = dict(_build_tests_valid_net_4_0_0(keys)) \
        if valid else \
        dict(_build_tests_invalid_net_4_0_0(keys))

    return {
        "manifest": {"type": "awses-decrypt-generate", "version": MANIFEST_VERSION},
        "keys": keys_uri,
        "plaintexts": {"small": 10 * 1024},
        "tests": tests,
    }


def main(args=None):
    """Entry point for CLI"""
    parser = argparse.ArgumentParser(
        description="Build an AWS Encryption SDK decrypt message generation manifest.")
    parser.add_argument("--human", action="store_true", help="Print human-readable JSON")
    parser.add_argument("--keys", required=True, help="Keys manifest to use")
    parser.add_argument("--valid", action="store_true",
                        help="Generate Valid or Invalid")

    parsed = parser.parse_args(args)

    manifest = build_manifest(parsed.keys, parsed.valid)

    kwargs = {}
    if parsed.human:
        kwargs["indent"] = 2

    print(json.dumps(manifest, **kwargs), file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
