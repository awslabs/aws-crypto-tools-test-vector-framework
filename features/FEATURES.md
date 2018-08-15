# Overview

For a general overview of the contents of this repository as well as a glossary of terms,
please see the [repository readme](../README.md).

# Features

These features describe the framework itself as well as the different types of supported manifests.
Some manifest definitions include helper scripts to generate a manifest if it is desirable to 
have a consistent starting point.

The intended purpose of manifests is to describe either how to generate test vectors or how to 
process existing test vectors. This enables compatible clients' testing frameworks to validate 
interoperability with other clients in a structured and reproducible way.

* [Framework](./0000-framework.md) : The overall AWS Crypto Tools test vector framework.
* [Meta Manifest](0001-meta.md) : A manifest for identifying one or more manifests
    that should be processed.
* [Keys Manifest](./0002-keys.md) : A storage location for test keys used for one or many
    test vectors.
    * [Manifest Generator](./0002-keys-generate.py) : Helper tool that will generate 
        a canonical keys manifest.
* [AWS Encryption SDK Full Ciphertext Encrypt](0003-awses-message-encryption.md) : A definition 
    of full ciphertext message test vectors to create.
    * [Manifest Generator](0003-awses-message-encryption-generate.py) : Helper tool that will 
      generate a canonical AWS Encryption SDK full ciphertext encrypt manifest using
      the keys manifest created by [0002-keys-generate.py](./0002-keys-generate.py).
* [AWS Encryption SDK Full Ciphertext Decrypt](0004-awses-message-decryption.md) : A definition 
    of existing full ciphertext message test vectors to decrypt.
* [AWS Encryption SDK Master Key](./0005-awses-master-key.md) : A format for defining master
    keys in AWS Encryption SDK manifests.
