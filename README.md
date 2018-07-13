# Overview

The AWS Crypto Tools test vector framework creates a mechanism for defining static test
vectors and associated manifests that describe those test vectors.

These test vectors are intended to be used to validate interoperability across implementations
of clients, primarily targeting those clients owned by AWS Crypto Tools.

# Features

These features describe the framework itself as well as the different types of supported manifests.
Some manifest definitions include helper scripts to generate a manifest if it is desirable to 
have a consistent starting point.

* [Framework](./features/0000-framework.md) : The overall AWS Crypto Tools test vector framework.
* [Meta Manifest](./features/0001-meta-manifest.md) : A manifest for identifying a group of manifests
  that should be processed as a group
* [Keys Manifest](./features/0002-keys.md) : A storage location for test keys used for one or many
  test vectors.
    * [Manifest Generator](./features/0002-keys-generate.py) : Helper tool that will generate 
      a standard keys manifest.
* [AWS Encryption SDK Full Ciphertext Encrypt](./features/0003-awses-encrypt.md) : A definition 
  of full ciphertext message test vectors to create.
    * [Manifest Generator](./features/0003-awses-encrypt-generate.py) : Helper tool that will 
      generate a standard AWS Encryption SDK full ciphertext encrypt manifest using the keys 
      manifest created by `0002-keys-generate.py`.
* [AWS Encryption SDK Full Ciphertext Decrypt](./features/0004-awses-decrypt.md) : A definition 
  of existing full ciphertext message test vectors to decrypt.
