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
    FRAME_SIZES,
    PLAINTEXTS,
    CRYPTOGRAPHIC_MATERIALS_MANAGER,
    RAW_RSA_PADDING_ALGORITHMS,
    UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    _providers,
    _raw_aes_providers,
)

MANIFEST_VERSION = 4

TAMPERINGS = (
    "truncate",
    "mutate",
    "half-sign",
)


def _build_tests(keys):
    """Build all tests to define in manifest, building from current rules and provided keys manifest.

    :param dict keys: Parsed keys manifest
    """
    for algorithm in ALGORITHM_SUITES:
        for frame_size in FRAME_SIZES:
            for ec in ENCRYPTION_CONTEXTS:
                for provider_set in _providers(keys):
                    for cmm in CRYPTOGRAPHIC_MATERIALS_MANAGER:
                        yield (
                            str(uuid.uuid4()),
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

    # for algorithm in ALGORITHM_SUITES:
    #     for frame_size in FRAME_SIZES:
    #         for ec in ENCRYPTION_CONTEXTS:
    #             for provider_set in _providers(keys):
    #                 yield (
    #                     str(uuid.uuid4()),
    #                     {
    #                         "encryption-scenario": {
    #                             "plaintext": "zero",
    #                             "algorithm": algorithm,
    #                             "frame-size": frame_size,
    #                             "encryption-context": ec,
    #                             "master-keys": provider_set,
    #                         }
    #                     },
    #                 )
    #
    # yield (
    #     str(uuid.uuid4()),
    #     {
    #         "encryption-scenario": {
    #             "plaintext": "tiny",
    #             "algorithm": "0178",
    #             "frame-size": 512,
    #             "encryption-context": UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    #             "master-keys": next(_raw_aes_providers(keys)),
    #         },
    #         "decryption-method": "streaming-unsigned-only",
    #     },
    # )
    #
    # yield (
    #     str(uuid.uuid4()),
    #     {
    #         "encryption-scenario": {
    #             "plaintext": "tiny",
    #             "algorithm": "0378",
    #             "frame-size": 512,
    #             "encryption-context": UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    #             "master-keys": next(_raw_aes_providers(keys)),
    #         },
    #         "decryption-method": "streaming-unsigned-only",
    #         "result": {
    #             "error": {"error-description": "Signed message input to streaming unsigned-only decryption method"}
    #         },
    #     },
    # )
    #
    # for tampering in TAMPERINGS:
    #     yield (
    #         str(uuid.uuid4()),
    #         {
    #             "encryption-scenario": {
    #                 "plaintext": "tiny",
    #                 "algorithm": "0478" if tampering == "half-sign" else "0578",
    #                 "frame-size": 512,
    #                 "encryption-context": UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    #                 "master-keys": next(_raw_aes_providers(keys)),
    #             },
    #             "tampering": tampering,
    #         },
    #     )
    #
    # yield (
    #     str(uuid.uuid4()),
    #     {
    #         "encryption-scenario": {
    #             "plaintext": "tiny",
    #             "algorithm": "0578",
    #             "frame-size": 512,
    #             "encryption-context": UNPRINTABLE_UNICODE_ENCRYPTION_CONTEXT,
    #             "master-keys": next(_raw_aes_providers(keys)),
    #         },
    #         "tampering": {"change-edk-provider-info": ["arn:aws:kms:us-west-2:658956600833:alias/EncryptOnly"]},
    #         "decryption-master-keys": [{"type": "aws-kms", "key": "us-west-2-encrypt-only"}],
    #     },
    # )


def build_manifest(keys_filename):
    """Build the test-case manifest which directs the behavior of cross-compatibility clients.

    :param str keys_file: Name of file containing the keys manifest
    """
    with open(keys_filename, "r") as keys_file:
        keys = json.load(keys_file)

    keys_path = "/".join(keys_filename.split(os.path.sep))
    keys_uri = urlunparse(("file", keys_path, "", "", "", ""))

    return {
        "manifest": {"type": "awses-decrypt-generate", "version": MANIFEST_VERSION},
        "keys": keys_uri,
        "plaintexts": PLAINTEXTS,
        "tests": dict(_build_tests(keys)),
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
