# Overview

For a general overview of the contents of this repository as well as a glossary of terms,
please see the [repository readme](../README.md).

## Version

This specification is currently at version 1.0.0

# Features

These features describe the AWS Crypto Tools test vector framework as well as the different
types of supported manifests.

The intended purpose of test vector manifests is to describe either how to generate test vectors
or how to process existing test vectors. This enables testing frameworks for compatible clients
to validate interoperability with other clients in a structured and reproducible way.

Some manifest definitions include helper scripts used to generate a manifest if it is desirable
to have a canonical representation of that manifest.

* [Framework](./0000-framework.md) : Describes the overall AWS Crypto Tools test vector framework.
* [Meta Manifest](0001-meta.md) : Describes a manifest for identifying one or more manifests
    that should be processed.
* [Keys Manifest](./0002-keys.md) : Describes a storage location for test keys used for one or many
    test vectors.
    * [Keys Manifest Generator](./0002-keys-generate.py) : Helper tool that will generate 
        a canonical keys manifest.
* [AWS Encryption SDK Message Encryption](0003-awses-message-encryption.md) : Describes a definition 
    of full AWS Encryption SDK ciphertext message test vectors to create.
    * [Message Encryption Manifest Generator](0003-awses-message-encryption-generate.py) : Helper tool that will 
      generate a canonical AWS Encryption SDK message encryption manifest using
      the keys manifest created by the [Keys Manifest Generator](./0002-keys-generate.py).
* [AWS Encryption SDK Message Decryption](0004-awses-message-decryption.md) : Describes a definition 
    of existing full AWS Encryption SDK ciphertext message test vectors to decrypt.
* [AWS Encryption SDK Master Key](./0005-awses-master-key.md) : Describes a format for defining master
    keys in AWS Encryption SDK manifests.
