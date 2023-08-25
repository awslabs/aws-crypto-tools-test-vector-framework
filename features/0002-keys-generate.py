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
import base64
import json
import sys

AWS_REGION = "us-west-2"
AWS_ACCOUNT_ID = "658956600833"

VERSION = 3
AES_KEYS = (
    (128, b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15"),
    (
        192,
        (b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16" b"\x17\x18\x19\x20\x21\x22\x23"),
    ),
    (
        256,
        (
            b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16"
            b"\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x30\x31"
        ),
    ),
)
RSA_KEYS = (
    (
        2048,
        "public",
        """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhJZkPbc7sDp/zO7m2/FS
SyIDpDh2lN1iubwgxOmZl+Zb7tGLVmezJo2NZFZKhXsLRYLyz2h/5m6kriyIiKVr
lPBbNDwVfvSq7TgD/oANE2NzxgCF+IdA9GSlSHEiUg7uRWbSJWpnKwem8eOF+fkA
celBlecnEmRNvsfYLzQbd63ce+fajJLKZ1qyYyDt6jJZo+Auzb56lRX2Qv7IKbN4
rQtfl5BUyCIt0O9RCOnQFZMGq/rSBlbZVldjKt1Mw/FjsZIlVetBGR1fZDhcDvYF
z3i7pLe2A3H3Ezy6XZraF34PrMbJhwE/EgUhqeXgC/BYmpJ5FNuLW5qaMUqNc3Aa
9QIDAQAB
-----END PUBLIC KEY-----""",
    ),
    (
        2048,
        "private",
        """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCElmQ9tzuwOn/M
7ubb8VJLIgOkOHaU3WK5vCDE6ZmX5lvu0YtWZ7MmjY1kVkqFewtFgvLPaH/mbqSu
LIiIpWuU8Fs0PBV+9KrtOAP+gA0TY3PGAIX4h0D0ZKVIcSJSDu5FZtIlamcrB6bx
44X5+QBx6UGV5ycSZE2+x9gvNBt3rdx759qMkspnWrJjIO3qMlmj4C7NvnqVFfZC
/sgps3itC1+XkFTIIi3Q71EI6dAVkwar+tIGVtlWV2Mq3UzD8WOxkiVV60EZHV9k
OFwO9gXPeLukt7YDcfcTPLpdmtoXfg+sxsmHAT8SBSGp5eAL8FiaknkU24tbmpox
So1zcBr1AgMBAAECggEBAIBdgmtl7TnvSTBF0+j5OO1Y3yGtMNFrjVu5UhiS+Yth
EXykDzz2ZTJcNZoBGWEmAYGpCB/aUonscS/YGdACJ6gpFIP77+vcQWgtpWBO5Vny
HXKDqzE08aQrlQIP1mSP5Av5QlfLLlswq2bhGyMq+k1OwZq6Es/xoHumzBzXXAh/
OHw64NukBP52vu7xwrjHj/0KRyJdWh0LojT2ai3xy2eEtzYa5Czoa9F+2hO9kzav
w9xp//eevSkArKb7ZkzSOZrO2liDeSI5F+7lQ/glPjCwnNg59oF+Iz9V9eWHVgOx
1xhq+LaHo9Dq+iT9W7kqDJkWV81wRt7ErDnp6vmo/TkCgYEA1jftYvawslQ+Xg65
SJFRAl2POODkLPsYEXoenIHsbq8GvrgTeGVVAqEMAHdLqgMMn0EkPphPiOCyT3Jt
9aZUbaZqFQ4MKem0ZOZ29SyFqgSPX5uXhkEubibMI88qloABRIrpbv+aGCVZ2q4g
s7bnGku+AiX5cfud3zxB1BdaxnMCgYEAnnKSx5tqS0GuDmC3RHj2esDOzzjW/iYu
eWMot6g2ndNQirgmNguV5hkAJfGzbHnyJMerIxcDkzXRJSbQt0sXAAufZ5HFcIWr
o4MFGae6wa89EJFXUkouaATYPfDfGz2o/HFpeSdy7IALXN4gHKCKuZ58mhmokk5X
ZsqhC6cQVvcCgYBWJ8wrvze1oTgsMBPI4dkI8IQHxjs+9AXsEYd6Pq7OnUpDLll2
VJrqIcdn8JLX374V1ucy3aMvU9+jIEylPa47I3EK4sl1me7Zne8+EBf6FzdqpnM8
pb58wtHbnRhtyzG3VX8pC1f4Wh1XXCz+2pL7+naC+q7mbuJBxERdfr8djQKBgERq
YGqD9u+r2oYmyLtuJ691VVcwydRPlD2hzVEP9xVKyzo6rXUkp4MFRIUdykWKmj27
YW/zXf3QfRA3pGOgrru8SQYlcUVW0nf1+NvNCtza19kxiKzljwgnH2APg6Z1h2QJ
bGt91ye7WiytVNxHjd78Sf0YGyuhXCfsUoF/j5SdAoGBAJ/x48q8ZacOclWmn44U
Tf8WLNwIC5eYqhG58Q1KmWY2R+7aq4bBsua72IBBjfEi6CKBgqNg1BZjyNVOu1if
YIErS0VT9tMptkHOcyXEjREuADCCveAAc96WeINmj//e1yGfnmYKjzuO2DNEXEZ7
dGvJibTIKmtjMlOjLwztqgLN
-----END PRIVATE KEY-----""",
    ),
    (
        3072,
        "private",
        """-----BEGIN PRIVATE KEY-----
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
iNT5B78WWDQPqJsjOtAPOA1k
----END PRIVATE KEY-----""",
    ),
    (
        3072,
        "public",
        """-----BEGIN PUBLIC KEY-----
MIIBojANBgkqhkiG9w0BAQEFAAOCAY8AMIIBigKCAYEAtxmP6r0zMx8CoWAnbARx
0IY6mZKeH9YRW5DQz82W8fF95LTOrqQuF8wKE/Qi6LuP7XZIoESiRPZyrRCpxTzG
7F3a8ND8GeVuO0uocc9UANq0LUR0A7pj+rXByn/xfRZtc7ZDV7FebSSeHIA+r8z/
MkjHAoNx8Bk98sRMWAKbAQy48gQ2jMu7IkQEuoGicev5kqCyQWqChPTns+Y8qN5D
8OI1JKoSlCdx1oDVBLhztQE8X0bFWJffkVE2t9574Q/y47q52gOLs31u4veJ8Bjv
h3zqM735x7EByt7TS+64s8XjrcdsGhiHVC9l9bY1AbMeKoA9mKOxkyo7PD13esFq
Ce/HlYPB8Qciz8OO/EuuO5I8CKwcvGiLfvyJCI7iL7jPAohMK4n41SN/0lQ1tKv/
oKSuu/DFTESXRizcNVvev377A8xmyyCpBxmoWtaKaCuGQCV4xCdCoMzMVvwhyDom
2qBz4YH3/MwY9Undd2gYgovSiASTicPXl/LI2G4N1hf3AgMBAAE=
-----END PUBLIC KEY-----"""
    ),
    (
        4096,
        "private",
        """-----BEGIN PRIVATE KEY-----
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
dzxtGxpeTBi+KhKlca8SlCdCqYwG6Q==
-----END PRIVATE KEY-----""",
    ),
    (
        4096,
        "public",
        """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAs7RoNYEPAIws89VV+kra
rVv/4wbdmUAaAKWgWuxZi5na9GJSmnhCkqyLRm7wPbQY4LCoa5/IMUxkHLsYDPdu
udY0Qm0GcoxOlvJKHYo4RjF7HyiS34D6dvyO4Gd3aq0mZHoxSGCxW/7hf03wEMzc
iVJXWHXhaI0lD6nrzIEgLrE4L+3V2LeAQjvZsTKd+bYMqeZOL2syiVVIAU8POwAG
GVBroJoveFm/SUp6lCiN0M2kTeyQA2ax3QTtZSAa8nwrI7U52XOzVmdMicJsy2Pg
uW98te3MuODdK24yNkHIkYameP/Umf/SJshUJQd5a/TUp3XE+HhOWAumx22tIDlC
vZS11cuk2fp0WeHUnXaC19N5qWKfvHEKSugzty/z3lGP7ItFhrF2X1qJHeAAsL11
kjo6Lc48KsE1vKvbnW4VLyB3wdNiVvmUNO29tPXwaR0Q5Gbr3jk3nUzdkEHouHWQ
41lubOHCCBN3V13mh/MgtNhESHjfmmOnh54ErD9saA1d7CjTf8g2wqmjEqvGSW6N
q7zhcWR2tp1olflS7oHzul4/I3hnkfL6Kb2xAWWaQKvg3mtsY2OPlzFEP0tR5UcH
Pfp5CeS1Xzg7hN6vRICW6m4l3u2HJFld2akDMm1vnSz8RCbPW7jp7YBxUkWJmypM
tG7Yv2aGZXGbUtM8o1cZarECAwEAAQ==
-----END PUBLIC KEY-----""",
    ),
)

AWS_KMS_KEYS = (
    (
        AWS_REGION + "-decryptable",
        "arn:aws:kms:" + AWS_REGION + ":" + AWS_ACCOUNT_ID + ":alias/EncryptDecrypt",
        True,
    ),
    (
        AWS_REGION + "-encrypt-only",
        "arn:aws:kms:" + AWS_REGION + ":" + AWS_ACCOUNT_ID + ":alias/EncryptOnly",
        False,
    ),
)


def build_manifest():
    """Build the manifest dictionary from the above key material definitions."""
    manifest = {"manifest": {"type": "keys", "version": VERSION}}
    keys = {}

    for key_bits, key_bytes in AES_KEYS:
        key_name = "aes-%s" % key_bits
        keys[key_name] = {
            "key-id": key_name,
            "encrypt": True,
            "decrypt": True,
            "algorithm": "aes",
            "type": "symmetric",
            "bits": key_bits,
            "encoding": "base64",
            "material": base64.b64encode(key_bytes).decode("utf-8"),
        }

    for key_bits, key_type, pem_key in RSA_KEYS:
        key_name = "rsa-%s-%s" % (key_bits, key_type)
        keys[key_name] = {
            "key-id": key_name,
            "encrypt": True,
            "decrypt": key_type == "private",
            "algorithm": "rsa",
            "type": key_type,
            "bits": key_bits,
            "encoding": "pem",
            "material": pem_key,
        }

    for key_name, key_arn, decryptable in AWS_KMS_KEYS:
        keys[key_name] = {
            "type": "aws-kms",
            "key-id": key_arn,
            "encrypt": True,
            "decrypt": decryptable,
        }

    manifest["keys"] = keys
    return manifest


def _test_manifest(manifest):
    """Test that the manifest is actually complete.

    :param dict manifest: keys manifest to test
    """
    for key, value in manifest["keys"].items():
        if "key-id" not in value:
            raise ValueError('Invalid key specification: "{}" does not define key ID.'.format(key))


def main(args=None):
    """Entry point for CLI"""
    parser = argparse.ArgumentParser(description="Build a keys manifest.")
    parser.add_argument("--human", action="store_true", help="Print human-readable JSON")

    parsed = parser.parse_args(args)

    manifest = build_manifest()
    _test_manifest(manifest)

    kwargs = {}
    if parsed.human:
        kwargs["indent"] = 4

    return json.dumps(manifest, **kwargs)


if __name__ == "__main__":
    sys.exit(main())
