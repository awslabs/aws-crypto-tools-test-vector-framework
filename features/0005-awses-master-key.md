
|           |                              |
|:----------|:-----------------------------|
|__Feature__|AWS Encryption SDK Master Key |
|__Version__|1                             |
|__Created__|2016-08-13                    |
|__Updated__|2018-08-13                    |

## Dependencies

This serves as a reference of all features that this feature depends on.

| Feature                                             | Min Version | Max Version |
|-----------------------------------------------------|-------------|-------------|
| [0002-keys](./0002-keys.md)                         | 1           | n/a         |

## Experimental Implementations

This serves as a reference for which implementations support this experimental feature. This
section should be removed once this feature is promoted from experimental status.

Unique implementations required for promotion: 2

| Repository                                                                         | Language | Pull Request                                             |
|------------------------------------------------------------------------------------|----------|----------------------------------------------------------|
| https://github.com/aws/aws-encryption-sdk-python/tree/master/test_vector_handlers  | Python   | https://github.com/aws/aws-encryption-sdk-python/pull/63 |
| Link to GitHub repository                                                          | Language | Pull request that added support                          |

## Supported Implementations

This serves as a references for which implementations support this feature. A minimum of two supporting implementations
are required for new feature versions.

| Repository                | Language | Feature Version                   | Minimum Version                                    | Pull Request                    |
|---------------------------|----------|-----------------------------------|----------------------------------------------------|---------------------------------|
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |

## Summary

The AWS Encryption SDK Master Key structure defines a standard way of describing master keys
as part of a manifest.

## Out of Scope

This file does not define any actual manifests, only a common structure that is used in AWS
Encryption SDK manifest definitions that need to include a description of a master key.

## Motivation

Several AWS Encryption SDK manifests have a requirement to define master keys that need to
be constructed while processing that manifest. In order to maintain consistency for these
definitions across manifest types, this file defines how master keys are defined in any
manifest type that needs to describe master keys.

## Guide-level Explanation

The master key structure is a JSON structure that identifies necessary characteristics
about an AWS Encryption SDK master key.

## Reference-level Explanation

### Contents

A master key structure is defined as a JSON object with the following members:

* `type` : Type of master key
    * Allowed Values
        * `aws-kms`
        * `raw`
* `key` : Name of key from a `keys` manifest
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
        * `sha384`
        * `sha512`

### Examples

```json
{
    "type": "aws-kms",
    "key": "us-west-2-decryptable"
}
```

```json
{
    "type": "raw",
    "provider-id": "aws-raw-vectors-persistant",
    "key": "rsa-4096-private",
    "encryption-algorithm": "rsa",
    "padding-algorithm": "oaep-mgf1",
    "padding-hash": "sha256"
}
```
