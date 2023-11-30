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
from urllib.parse import urlunparse

from awses_message_encryption_utils import (
    ALGORITHM_SUITES,
    ENCRYPTION_CONTEXTS,
    FRAME_SIZES,
    PLAINTEXTS,
    RAW_RSA_PADDING_ALGORITHMS,
    _keys_for_algorithm,
    _keys_for_decryptval,
    _keys_for_type,
    build_tests,
)

MANIFEST_VERSION = 2


def _tests_for_type(type_name, tests):
    """Filter encrypt manifest keys by type.

    :param str type_name: Key type name for which to filter
    :param dict keys: Parsed keys manifest
    """
    for _name, test in tests["tests"].items():
        for master_key in test["master-keys"]:
            if master_key["type"] == type_name:
                yield test
                break


def _tests_for_algorithm(algorithm_name, tests):
    """Filter encrypt manifest keys by algorithm name.

    :param str algorithm_name: Key algorithm name for which to filter
    :param dict tests: Full message encrypt manifest to test
    """
    for _name, test in tests["tests"].items():
        for master_key in test["master-keys"]:
            if master_key["key"].startswith(algorithm_name + "-"):
                yield test
                break


def _test_manifest(keys_filename, manifest):
    """Test that the manifest is actually complete.

    :param str keys_file: Name of file containing the keys manifest
    :param dict manifest: Full message encrypt manifest to test
    """
    with open(keys_filename, "r") as keys_file:
        keys = json.load(keys_file)

    aes_key_count = len(list(_keys_for_algorithm("aes", keys)))
    black_hole_aes_key_count = len(
        [value for value in list(_keys_for_algorithm("aes", keys)) if value in list(_keys_for_decryptval(False, keys))]
    )
    aes_key_combination_count = (
        aes_key_count
        - black_hole_aes_key_count
        + ((aes_key_count - black_hole_aes_key_count) * black_hole_aes_key_count)
    )

    cycleable_rsa_key_count = 0
    black_hole_rsa_key_count = 0
    for _name, rsa_key in _keys_for_algorithm("rsa", keys):
        if rsa_key["encrypt"]:
            if rsa_key["decrypt"]:
                cycleable_rsa_key_count += 1
            else:
                black_hole_rsa_key_count += 1

    cycleable_rsa_combination_count = cycleable_rsa_key_count * len(RAW_RSA_PADDING_ALGORITHMS)
    black_hole_rsa_combination_count = cycleable_rsa_combination_count * black_hole_rsa_key_count
    rsa_key_combination_count = cycleable_rsa_combination_count + black_hole_rsa_combination_count

    kms_key_count = len(list(_keys_for_type("aws-kms", keys)))
    black_hole_kms_key_count = len(
        [value for value in list(_keys_for_type("aws-kms", keys)) if value in list(_keys_for_decryptval(False, keys))]
    )
    kms_key_combination_count = (
        kms_key_count
        - black_hole_kms_key_count
        + ((kms_key_count - black_hole_kms_key_count) * black_hole_kms_key_count)
    )

    aes_test_count = len(list(_tests_for_algorithm("aes", manifest)))
    rsa_test_count = len(list(_tests_for_algorithm("rsa", manifest)))
    kms_test_count = len(list(_tests_for_type("aws-kms", manifest)))

    iterations = len(ALGORITHM_SUITES) * len(FRAME_SIZES) * len(ENCRYPTION_CONTEXTS)
    expected_aes_test_count = aes_key_combination_count * iterations
    expected_rsa_test_count = rsa_key_combination_count * iterations
    expected_kms_test_count = kms_key_combination_count * iterations

    if not all(
        [
            0 < expected_aes_test_count == aes_test_count,
            0 < expected_rsa_test_count == rsa_test_count,
            0 < expected_kms_test_count == kms_test_count,
        ]
    ):
        raise ValueError(
            "Unexpected test count: \nAES: {aes}\nRSA: {rsa}\nAWS-KMS: {kms}".format(
                aes="Expected: {expected} Actual: {actual}".format(
                    expected=expected_aes_test_count, actual=aes_test_count
                ),
                rsa="Expected: {expected} Actual: {actual}".format(
                    expected=expected_rsa_test_count, actual=rsa_test_count
                ),
                kms="Expected: {expected} Actual: {actual}".format(
                    expected=expected_kms_test_count, actual=kms_test_count
                ),
            )
        )


def build_manifest(keys_filename):
    """Build the test-case manifest which directs the behavior of cross-compatibility clients.

    :param str keys_file: Name of file containing the keys manifest
    """
    with open(keys_filename, "r") as keys_file:
        keys = json.load(keys_file)

    keys_path = "/".join(keys_filename.split(os.path.sep))
    keys_uri = urlunparse(("file", keys_path, "", "", "", ""))

    return {
        "manifest": {"type": "awses-encrypt", "version": MANIFEST_VERSION},
        "keys": keys_uri,
        "plaintexts": PLAINTEXTS,
        "tests": dict(build_tests(keys)),
    }


def main(args=None):
    """Entry point for CLI"""
    parser = argparse.ArgumentParser(description="Build an AWS Encryption SDK encrypt message manifest.")
    parser.add_argument("--human", action="store_true", help="Print human-readable JSON")
    parser.add_argument("--keys", required=True, help="Keys manifest to use")

    parsed = parser.parse_args(args)

    manifest = build_manifest(parsed.keys)

    _test_manifest(parsed.keys, manifest)

    kwargs = {}
    if parsed.human:
        kwargs["indent"] = 2

    print(json.dumps(manifest, **kwargs), file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
