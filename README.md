# Overview

The AWS Cryptography test vector framework creates a mechanism for defining static test
vectors and associated manifests that describe those test vectors.

These test vectors are intended to be used to validate interoperability across implementations
of clients, primarily targeting those clients owned by AWS Crypto Tools.

# Features

* [Framework](./features/0000-framework.md) : The overall AWS Cryptography test vector framework.
* [Meta Manifest](./features/0001-meta-manifest.md) : A manifest for identifying a group of manifests
  that should be processed as a group
* [Keys Manifest](./features/0002-keys.md) : A storage location for test keys used for one or many
  test vectors.
* [AWS Encryption SDK Full Ciphertext Encrypt](./features/0003-awses-encrypt.md) : A definition 
  of full ciphertext message test vectors to create.
* [AWS Encryption SDK Full Ciphertext Decrypt](./features/0004-awses-decrypt) : A definition 
  of existing full ciphertext message test vectors to decrypt.
