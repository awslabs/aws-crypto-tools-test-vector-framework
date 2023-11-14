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
    ENCRYPTION_CONTEXTS,
    EMPTY_ENCRYPTION_CONTEXT,
    FRAME_SIZES,
    PLAINTEXTS,
    CRYPTOGRAPHIC_MATERIALS_MANAGER,
    RAW_RSA_PADDING_ALGORITHMS,
    UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    _providers,
    _raw_aes_providers, NON_UNICODE_ENCRYPTION_CONTEXT,
)

MANIFEST_VERSION = 4

TAMPERINGS = (
    "truncate",
    "mutate",
    "half-sign",
)


def _ec_name(ec: dict[str, str]) -> str:
    return f'ec_len_{len(ec)}'


def _build_tests(keys):
    """Build all tests to define in manifest,
    building from current rules and provided keys manifest.

    :param dict keys: Parsed keys manifest
    """
    # RequiredEncryptionContextCMM requires EC,
    # so remove Empty EC and handle it below
    filtered_ec = list(filter(lambda _ec: EMPTY_ENCRYPTION_CONTEXT != _ec, ENCRYPTION_CONTEXTS))
    print(f'Debug: Not Empty in Filtered? '
          f'{NON_UNICODE_ENCRYPTION_CONTEXT in filtered_ec}',
          file=sys.stderr)
    for cmm in CRYPTOGRAPHIC_MATERIALS_MANAGER:
        for ec in filtered_ec:
            for algorithm in ALGORITHM_SUITES:
                for frame_size in FRAME_SIZES:
                    for provider_set in _providers(keys):
                        yield (
                            f"{algorithm}-{_ec_name(ec)}-{str(uuid.uuid4())}",
                            {
                                "encryption-scenario": {
                                    "plaintext": "small",
                                    "algorithm": algorithm,
                                    "frame-size": frame_size,
                                    "encryption-context": ec,
                                    "master-keys": provider_set,
                                    "cmm": cmm
                                }
                            },
                        )
    # print(f'Debug: Default? {"Default" in CRYPTOGRAPHIC_MATERIALS_MANAGER} and '
    #       f'Empty? {EMPTY_ENCRYPTION_CONTEXT in ENCRYPTION_CONTEXTS}',
    #       file=sys.stderr)
    # print(f'Debug: Required? {"RequiredEncryptionContext" in CRYPTOGRAPHIC_MATERIALS_MANAGER} and '
    #       f'Not Empty? {NON_UNICODE_ENCRYPTION_CONTEXT in ENCRYPTION_CONTEXTS}',
    #       file=sys.stderr)


def _empty_ec_default_cmm_helper(keys):
    ec = EMPTY_ENCRYPTION_CONTEXT
    for algorithm in ALGORITHM_SUITES:
        for frame_size in FRAME_SIZES:
            for provider_set in _providers(keys):
                yield (
                    f"{algorithm}-{_ec_name(ec)}-{str(uuid.uuid4())}",
                    {
                        "encryption-scenario": {
                            "plaintext": "small",
                            "algorithm": algorithm,
                            "frame-size": frame_size,
                            "encryption-context": ec,
                            "master-keys": provider_set,
                            "cmm": "Default"
                        }
                    },
                )


def build_manifest(keys_filename):
    """Build the test-case manifest which directs the behavior of cross-compatibility clients.

    :param str keys_file: Name of file containing the keys manifest
    """
    with open(keys_filename, "r") as keys_file:
        keys = json.load(keys_file)

    keys_path = "/".join(keys_filename.split(os.path.sep))
    keys_uri = urlunparse(("file", keys_path, "", "", "", ""))
    tests = dict(_build_tests(keys))
    print(f'Debug: Test Size {len(tests)}', file=sys.stderr)
    print(f'Debug: Default? {"Default" in CRYPTOGRAPHIC_MATERIALS_MANAGER} and '
          f'Empty? {EMPTY_ENCRYPTION_CONTEXT in ENCRYPTION_CONTEXTS}',
          file=sys.stderr)
    if "Default" in CRYPTOGRAPHIC_MATERIALS_MANAGER and \
            EMPTY_ENCRYPTION_CONTEXT in ENCRYPTION_CONTEXTS:
        tests.update(_empty_ec_default_cmm_helper(keys))
    print(f'Debug: Test Size {len(tests)}', file=sys.stderr)

    return {
        "manifest": {"type": "awses-decrypt-generate", "version": MANIFEST_VERSION},
        "keys": keys_uri,
        "plaintexts": PLAINTEXTS,
        "tests": tests,
    }


def main(args=None):
    """Entry point for CLI"""
    parser = argparse.ArgumentParser(description="Build an AWS Encryption SDK decrypt message generation manifest.")
    parser.add_argument("--human", action="store_true", help="Print human-readable JSON")
    parser.add_argument("--keys", required=True, help="Keys manifest to use")

    parsed = parser.parse_args(args)

    manifest = build_manifest(parsed.keys)

    kwargs = {}
    if parsed.human:
        kwargs["indent"] = 4

    print(json.dumps(manifest, **kwargs), file=sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
