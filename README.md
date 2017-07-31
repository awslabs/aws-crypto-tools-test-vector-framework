# Overview
The AWS Encryption SDK Cross-Compatibility Framework defines requirements for operation and
behavior of AWS Encryption SDK clients when generating and reading ciphertext test cases for
cross-compatibility testing.  This provides a standard approach for clients in different
languages to verify that they are compatible with each other.

A static, known-good, set of output ciphertext is collected into the static cross-compatiblity
test resources repository for use in unit tests across clients.

__Write__

1. Read test case manifest.
2. Generate plaintexts and upload to S3 bucket.
2. Generate all required test cases for each plaintext, uploading ciphertext to S3 bucket.
3. If not already in bucket, upload any plaintext used to S3 bucket.
4. Generate below described ciphertext manifest file and write to S3 bucket.
5. Generate below described results manifest file and write to S3 bucket.

__Read__

1. Read ciphertext manifest file.
2. Using data in ciphertext manifest, decrypt all test cases and validate the results against their respective plaintexts.

# Local File Writing
When writing out results of a test run to a local filesystem, all files must be written under a single
root directory.  All manifest files must be written in a `manifests` directory within that root directory.

## Example
```
manifests/test_case.manifest
manifests/ciphertext.manifest
plaintext/small
ciphertext/0014/small/10240/49a4917b5cdd4b54bb9d319b55ffe5ad
ciphertext/0046/small/10240/3148829c48b8497ea1371c19323a6c45
ciphertext/0078/small/512/45453146ee9543f58205d2780bdea8ec
ciphertext/0114/small/512/3e414f28dacd4e49912c72f4dda37460
ciphertext/0146/small/512/ca7e91c45f6a4b8ba571ee1ef596b0cc
ciphertext/0178/small/512/28213b6698c54222ab0ef2d281fb72bf
ciphertext/0214/small/20480/6a8e7b712adc4f828096cd28c2a2fd98
ciphertext/0346/small/20480/e41141acfc294871adb3cd4af40a41dd
ciphertext/0378/small/20480/11c50caa1eed4ea99edb724c6bff5b9b
```

# Static Raw Master Key Provider
A cross-compatibility testing suite must define two Raw Master Key Providers: one with with provider
id `static-aws-xcompat` which provides pre-defined Master Keys, and one with provider id
`ephemeral-aws-xcompat` which provides random Master Keys. The Master Keys provided by
`static-aws-xcompat` do not need to be consistent across runs, but must be consistent for all calls
within a single test run for every unique combination of `key_bits` and `encryption_algorithm` in
the ciphertext manifest test-case definition.

# Test Case Manifest
The test case manifest defines which test cases cross compatibility clients should generate.

## Scenarios to test

###Algorithms
* Every Master Algorithm

###Framing
* Non-framed message
* Framed message with frame size smaller than plaintext size
* Framed message with frame size equal to plaintext size
* Framed message with frame size larger than plaintext size
* Framed message with >10 frames

###Encryption Context
* Message without encryption context
* Message with encryption context
* Unicode values in encryption context
* No unicode values in encryption context
* Binary values in encryption context
* No binary values in encryption context

###Master Key Providers
* Single KMS MasterKey which can be decrypted by all consumers
* Multiple KMS MasterKeys, of which only one can be decrypted by all consumers
* Single AES Symmetric Static Raw MasterKey as described above, which can be decrypted
* Multiple Symmetric Raw MasterKeys as described above, only one of which can be decrypted
* Single RSA Asymmetric Static Raw MasterKey as described above, which can be decrypted
* Multiple Asymmetric Raw MasterKeys as described above, only one of which can be decrypted

## Generation
This manifest should be generated using the `generate_manifest` script in this package.

## Naming
The filename or S3 Key of this manifest should have a suffix of `.test_case.manifest`

## Contents
### manifest
Identifies this manifest.

* `type` : Identifies the type of manifest
   * Must be `test_case`

### plaintexts
List of descriptions of plaintext sources to generate.
The specific contents of any given plaintext is left to the developer of each client.

* `name` : Identifying name for plaintext source
* `multiple` : Number of `multiplier` bytes to generate
* `multiplier` : Multiplier for `multiple`
   * Allowed Values
      * `B` : `1`
      * `K` : `1024`
      * `M` : `1024 * 1024`

### test_scenarios
List containing objects describing each test scenario.

* `plaintext` : Plaintext source name
* `algorithm` : Hex string of supported [Algorithm ID](http://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/algorithms-def.html)
* `framed_body` : Boolean stating whether ciphertext message body should be framed
* `frame_size` : Frame size in bytes (required if framed_body is true)
* `encryption_context` : Map of keys and values to use for encryption context
* `master_keys` : List of Master Key descriptions:
   * `provider_id` : Provider ID of Master Key Provider to use
   * `decryptable` : Boolean stating whether consumers should be able to decrypt data keys encrypted by this MasterKey
   * `key_id`: Key ID from provider to use (required for AWS KMS Master Keys)
   * `encryption_algorithm` : Encryption Algorithm (required for Static Raw Master Keys)
      * Allowed Values
         * `AES`
         * `RSA`
   * `key_bits` : Master Key size in bits (required for Asymmetric Static Raw Master Keys)
   * `padding_algorithm` : Padding Algorithm (required for RSA Static Raw Master Keys)
      * Allowed Values
         * `PKCS1`
         * `OAEP-MGF1`
   * `padding_hash` : Hash Algorithm used with Padding Algorithm (required for OAEP-MGF1)
      * Allowed Values
         * `SHA-1`
         * `SHA-256`

## Example
```json
{
    "manifest": {
        "type": "test-case"
    },
    "plaintexts": [
        {
            "name": <string>,
            "multiple": <int>,
            "multiplier": <string>
        }
    ],
    "test_scenarios": [
        {
            "plaintext": <string>,
            "algorithm": <string>,
            "framed_body": <boolean>,
            "frame_size": <int>,
            "encryption_context": <object>,
            "master_keys": [
                {
                    "provider_id": <string>,
                    "decryptable": <boolean>,
                    "key_id": <string>,
                    "encryption_algorithm": <string>,
                    "key_bits": <int>,
                    "padding_algorithm": <string>,
                    "padding_hash": <string>
                }
            ]
        }
    ]
}
```

# Results Manifest
Each cross-compatibility test suite should create a results manifest file describing the
results of running each test scenario.

## Naming
The filename or S3 Key of this manifest should have a suffix of `.results.manifest`

## Contents
### manifest
Identifies this manifest and any associated manifests.

* `type` : Identifies the type of manifest
   * Must be `results`
* `test_case` : Identifies the Test Case Manifest used to create the ciphertexts referenced in this manifest (either
filename or bucket/key required)
  * `filename` : Local filename relative to test scenario root
  * `bucket` : S3 Bucket
  * `key` : S3 Key
  * `version_id` : S3 Object Version (optional)
* `ciphertext` : Identifies the Ciphertext Manifest associated with these results (either filename or bucket/key
required)
  * `filename` : Local filename relative to test scenario root
  * `bucket` : S3 Bucket
  * `key` : S3 Key
  * `version_id` : S3 Object Version (optional)

### client
Identifies the client used when running these test cases.

* `name`: Identifies the client
  * If the client is on github, must the the full github repository name (ex: `awslabs/aws-encryption-sdk-python`)
* `version`: Identifies the client version

### test_cases
List containing object describing each test scenario and the results of that scenario.

* `description` : Description of ciphertext test case (optional)
* `plaintext` : Plaintext source description from Test Case Manifest
* `test_scenario` : Test scenario description from Test Case Manifest
* `results` : Description of results
   * `status` : Describes the final results
      * Allowed Values
         * `SUCCESS`
         * `FAIL`
   * `error` : Required if `status` is `FAIL`
      * `type` : Identifying short name for type of error encountered (ex: error class name)
      * `description` : Message describing the specific error encountered (ex: error arguments)

## Example
```json
{
    "manifest": {
        "type": "results",
        "test_case": {
            "bucket": <string>,
            "key": <string>,
            "version_id": <string>
        },
        "ciphertext": {
            "bucket": <string>,
            "key": <string>,
            "version_id": <string>
        }
    },
    "client": {
        "name": <string>,
        "version": <string>
    },
    "test_cases": [
        {
            "description": <string>,
            "plaintext": <object>,
            "test_scenario": <object>,
            "results": {
                "status": <string>,
                "error": {
                    "type": <string>,
                    "description": <string>
                }
            }
        }
    ]
}
```

# Ciphertext Manifest
Each cross-compatibility test suite should create a ciphertext manifest file describing the
generated ciphertext files. The information contained in this manifest should contain all
necessary information as described below for a compatible cross-compatibility testing suite
to successfully decrypt all referenced ciphertext.

> __NOTE:__ Only successful encryptions should be recorded in the ciphertext manifest.

## Naming
The filename or S3 Key of this manifest should have a suffix of `.ciphertext.manifest`

## Contents
### manifest
Identifies this manifest and any associated manifests.

* `type` : Identifies the type of manifest
   * Must be `ciphertext`
* `test_case` : Identifies the Test Case Manifest used to create the ciphertexts referenced in this
manifest (either filename or bucket/key required)
  * `filename` : Local filename relative to test scenario root
  * `bucket` : S3 Bucket
  * `key` : S3 Key
  * `version_id` : S3 Object Version (optional)

### client
Identifies the client used when running these test cases.

* `name`: Identifies the client
  * If the client is on github, must the the github repository name (ex: `awslabs/aws-encryption-sdk-python`)
* `version`: Identifies the client version

### test_cases
List containing objects describing each generated ciphertext objects.

* `description` : Description of ciphertext test case (optional)
* `algorithm` : Hex string of supported [Algorithm ID](http://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/algorithms-def.html) used
* `plaintext` : identifies the S3 object containing generated plaintext object in this bucket
  * `filename` : Local filename relative to test scenario root (either filename or bucket/key required)
  * `bucket` : S3 Bucket
  * `key` : S3 Key
  * `version_id` : S3 Object Version (optional)
* `ciphertext` : identifies the S3 object containing generated ciphertext object in this bucket
  * `filename` : Local filename relative to test scenario root (either filename or bucket/key required)
  * `bucket` : S3 Bucket
  * `key` : S3 Key
  * `version_id` : S3 Object Version (optional)
* `master_keys` : List of Master Key descriptions:
  * `provider_id` : Master Key Provider ID
  * `key_id` : Master Key ID (required for AWS KMS Master Keys)
  * `key_bits` : Key size in bits (required for Asymmetric Static Raw Master Keys)
  * `encryption_algorithm` : Encryption Algorithm (required for Static Raw Master Keys)
     * Allowed Values
         * `AES`
         * `RSA`
  * `padding_algorithm` : Padding Algorithm (required for RSA Static Raw Master Keys)
     * Allowed Values
         * `PKCS1`
         * `OAEP-MGF1`
  * `padding_hash` : Hash Algorithm used with Padding Algorithm (required if `padding_algorithm` is `OAEP-MGF1`)
     * Allowed Values
         * `SHA-1`
         * `SHA-256`

### test_keys
Contains keys used by Static Raw Master Key Providers when generating ciphertext. 

* `<encryption type>`
   * `<key bits>`
      * `<key object>`

Keys are stored as JSON objects with the following attributes:

* `encoding` : Encoding used to store key
   * Allowed Values
      * `raw`
      * `base64`
      * `pem`
* `line_separator` : Line separator with which to join multi-line keys (optional) (default: "")
* `key` : List containing elements which make up key

> __NOTE:__ For asymmetric keys, only the private key is stored.

## Example
```json
{
    "manifest": {
        "type": "ciphertext",
        "test_case": {
            "bucket": <string>,
            "key": <string>,
            "version_id": <string>
        }
    },
    "client": {
        "name": "awslabs/aws-encryption-sdk-python",
        "version": "1.2.0"
    },
    "test_cases": [
        {
            "description": <string>,
            "algorithm": <string>,
            "plaintext": {
                "bucket": <string>,
                "key": <string>,
                "version_id": <string>
            },
            "ciphertext": {
                "bucket": <string>,
                "key": <string>,
                "version_id": <string>
            },
            "master_keys": [
                {
                    "provider_id": <string>,
                    "key_id": <string>,
                    "encryption_algorithm": <string>,
                    "key_bits": <int>,
                    "padding_algorithm": <string>,
                    "padding_hash": <string>
                }
            ]
        }
    ],
    "test_keys": {
        "aes": {
            "128": {
                "encoding": "raw",
                "key": ["1234567890123456"]
            },
            "192": {
                "encoding": "raw",
                "key": ["123456789012345678901234"]
            },
            "256": {
                "encoding": "base64",
                "key": ["yar+8MbgZemJ9j41RjNpiYVCblujSNkYTIeKC/EEADc="]
            }
        },
        "rsa": {
            "2048": {
                "encoding": "pem",
                "line_separator": "\n", 
                "key": [
                    "-----BEGIN RSA PRIVATE KEY-----",
                    "MIIEowIBAAKCAQEAo8uCyhiO4JUGZV+rtNq5DBA9Lm4xkw5kTA3v6EPybs8bVXL2",
                    "ZE6jkbo+xT4Jg/bKzUpnp1fE+T1ruGPtsPdoEmhY/P64LDNIs3sRq5U4QV9IETU1",
                    "vIcbNNkgGhRjV8J87YNY0tV0H7tuWuZRpqnS+gjV6V9lUMkbvjMCc5IBqQc3heut",
                    "/+fH4JwpGlGxOVXI8QAapnSy1XpCr3+PT29kydVJnIMuAoFrurojRpOQbOuVvhtA",
                    "gARhst1Ji4nfROGYkj6eZhvkz2Bkud4/+3lGvVU5LO1vD8oY7WoGtpin3h50VcWe",
                    "aBT4kejx4s9/G9C4R24lTH09J9HO2UUsuCqZYQIDAQABAoIBAQCfC90bCk+qaWqF",
                    "gymC+qOWwCn4bM28gswHQb1D5r6AtKBRD8mKywVvWs7azguFVV3Fi8sspkBA2FBC",
                    "At5p6ULoJOTL/TauzLl6djVJTCMM701WUDm2r+ZOIctXJ5bzP4n5Q4I7b0NMEL7u",
                    "ixib4elYGr5D1vrVQAKtZHCr8gmkqyx8Mz7wkJepzBP9EeVzETCHsmiQDd5WYlO1",
                    "C2IQYgw6MJzgM4entJ0V/GPytkodblGY95ORVK7ZhyNtda+r5BZ6/jeMW+hA3VoK",
                    "tHSWjHt06ueVCCieZIATmYzBNt+zEz5UA2l7ksg3eWfVORJQS7a6Ef4VvbJLM9Ca",
                    "m1kdsjelAoGBANKgvRf39i3bSuvm5VoyJuqinSb/23IH3Zo7XOZ5G164vh49E9Cq",
                    "dOXXVxox74ppj/kbGUoOk+AvaB48zzfzNvac0a7lRHExykPH2kVrI/NwH/1OcT/x",
                    "2e2DnFYocXcb4gbdZQ+m6X3zkxOYcONRzPVW1uMrFTWHcJveMUm4PGx7AoGBAMcU",
                    "IRvrT6ye5se0s27gHnPweV+3xjsNtXZcK82N7duXyHmNjxrwOAv0SOhUmTkRXArM",
                    "6aN5D8vyZBSWma2TgUKwpQYFTI+4Sp7sdkkyojGAEixJ+c5TZJNxZFrUe0FwAoic",
                    "c2kb7ntaiEj5G+qHvykJJro5hy6uLnjiMVbAiJDTAoGAKb67241EmHAXGEwp9sdr",
                    "2SMjnIAnQSF39UKAthkYqJxa6elXDQtLoeYdGE7/V+J2K3wIdhoPiuY6b4vD0iX9",
                    "JcGM+WntN7YTjX2FsC588JmvbWfnoDHR7HYiPR1E58N597xXdFOzgUgORVr4PMWQ",
                    "pqtwaZO3X2WZlvrhr+e46hMCgYBfdIdrm6jYXFjL6RkgUNZJQUTxYGzsY+ZemlNm",
                    "fGdQo7a8kePMRuKY2MkcnXPaqTg49YgRmjq4z8CtHokRcWjJUWnPOTs8rmEZUshk",
                    "0KJ0mbQdCFt/Uv0mtXgpFTkEZ3DPkDTGcV4oR4CRfOCl0/EU/A5VvL/U4i/mRo7h",
                    "ye+xgQKBgD58b+9z+PR5LAJm1tZHIwb4tnyczP28PzwknxFd2qylR4ZNgvAUqGtU",
                    "xvpUDpzMioz6zUH9YV43YNtt+5Xnzkqj+u9Mr27/H2v9XPwORGfwQ5XPwRJz/2oC",
                    "EnPmP1SZoY9lXKUpQXHXSpDZ2rE2Klt3RHMUMHt8Zpy36E8Vwx8o",
                    "-----END RSA PRIVATE KEY-----"
                ]
            }
        }
    }
}
```