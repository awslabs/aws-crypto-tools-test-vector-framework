
|           |                                               |
|:----------|:----------------------------------------------|
|__Feature__|AWS Encryption SDK Decrypt Message             |
|__Version__|1                                              |
|__Created__|2018-06-25                                     |
|__Updated__|ISO-8601 date feature was most recently updated|

## Dependencies

This serves as a reference of all features that this feature depends on.

| Feature                  | Min Version                              | Max Version                              |
|--------------------------|------------------------------------------|------------------------------------------|
| Name and link to feature | Minimum version required by this feature | Maximum version required by this feature |
| Name and link to feature | Minimum version required by this feature | Maximum version required by this feature |

## Experimental Implementations

This serves as a reference for which implementations support this experimental feature. This
section should be removed once this feature is promoted from experimental status.

Unique implementations required for promotion: 2

| Repository                | Language | Pull Request                    |
|---------------------------|----------|---------------------------------|
| Link to GitHub repository | Language | Pull request that added support |
| Link to GitHub repository | Language | Pull request that added support |

## Supported Implementations

This serves as a references for which implementations support this feature. A minimum of two supporting implementations
are required for new feature versions.

| Repository                | Language | Feature Version                   | Minimum Version                                    | Pull Request                    |
|---------------------------|----------|-----------------------------------|----------------------------------------------------|---------------------------------|
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |

## Summary

The AWS Encryption SDK Decrypt Manifest defines static test vectors for full AWS Encryption SDK 
ciphertext messages along with sufficient metadata to decrypt them.

## Out of Scope

These manifests do not include any direct full description of how the test vectors were created. 
That is covered by 0003-awses-encrypt.

## Motivation

We need a way of describing full AWS Encryption SDK ciphertext message test vectors and how to 
decrypt them. This will be used both for decrypting known good test vectors with an unknown implementation 
and for decrypting with a known good implementation ciphertexts created by an unknown implementation.

## Guide-level Explanation

This manifest describes test cases of full AWS Encryption SDK ciphertext messages and corresponding 
plaintext. Each test definition includes metadata that defines the master key required for decryption.

In addition to describing the test cases, the manifest also identifies the client and version 
that created the ciphertext.

### Workflow

1. Read decrypt manifest file.
2. Using data in decrypt manifest, decrypt all test vectors and validate the results against their respective plaintexts.


## Reference-level Explanation

### Contents

#### manifest

Map identifying this manifest.

* `type` : Identifies this manifest as a meta-manifest.
    * Must be `awses-decrypt`
* `version` : Identifies the version of this document that describes the contents of the manifest.

#### encrypt-manifest

URI that identifies the AWS Encryption SDK encrypt manifest that was used to generate these test 
cases. This is used if necessary to identify the rules that were used to generate a specific 
test case.

#### client

Identifies the client used to generate these test vectors.

* `name`: Identifies the client
  * If the client is on github, must the the github repository name (ex: `awslabs/aws-encryption-sdk-python`)
* `version`: Identifies the client version

#### keys

URI identifying a keys manifest to use with all tests.

#### tests

Map object mapping a test case ID to a test case description that describes a test vector.

The test case map name must have a matching entry in an AWS Encryption SDK encrypt manifest. 
This can be used to determine what criteria were used to generate a given test case.

* `description` : Description of ciphertext test case (optional)
* `plaintext` : URI that identifies the plaintext
* `ciphertext` : URI that identifies the ciphertext
* `master-keys` : List of Master Key descriptions:
   * `type` : Type of master key
     * Allowed Values
       * `aws-kms`
       * `raw`
   * `key` : Name of key from `keys` manifest
   * `key-id` : Master Key ID (optional) (default: `key` name or `key.key-id` for AWS KMS)
   * `provider-id` : Master Key Provider ID (required for Raw Master Keys)
   * `encryption-algorithm` : Encryption Algorithm (required for Raw Master Keys)
      * Allowed Values
          * `aes`
          * `rsa`
   * `padding-algorithm` : Padding Algorithm (required for RSA Raw Master Keys)
      * Allowed Values
          * `pkcs1`
          * `oaep-mgf1`
   * `padding-hash` : Hash Algorithm used with Padding Algorithm (required if `padding-algorithm` is `oaep-mgf1`)
      * Allowed Values
          * `sha1`
          * `sha256`
          * `sha512`

### Example

```json
{
    "manifest": {
        "type": "awses-decrypt",
        "version": 1
    },
    "encrypt-manifest": "file://relative/file/path.json",
    "client": {
        "name": "awslabs/aws-encryption-sdk-python",
        "version": "1.3.4"
    },
    "keys": "file://relative/file/path.json",
    "tests": {
        "2d1e0da9-74f8-4817-842d-c2b973abed7c": {
            "description": "Single raw rsa provider encryption",
            "plaintext": "file://relative/path/to/plaintext",
            "ciphertext": "file://relative/path/to/ciphertext",
            "master-keys": [
                {
                    "type": "raw",
                    "provider-id": "aws-raw-vectors-persistant",
                    "key": "rsa-2048",
                    "encryption-algorithm": "rsa",
                    "padding-algorithm": "oaep-mgf1",
                    "padding-hash": "sha256"
                }
            ]
        },
        "f7f3416b-7527-4108-8d15-6d0d5a377a2c": {
            "description": "Single aws kms provider encryption",
            "plaintext": "file://relative/path/to/plaintext",
            "ciphertext": "file://relative/path/to/ciphertext",
            "master-keys": [
                {
                    "type": "aws-kms",
                    "key": "us-west-2-decryptable"
                }
            ]
        }
    }
}
```
