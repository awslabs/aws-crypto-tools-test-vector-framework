# Overview

This repository contains the AWS Crypto Tools test vector framework specification. The purpose
of this specification is to provide a common mechanism for defining the structure and properties
of test vector manifests. These manifests in turn provide information about how to either generate
new test vectors or process existing test vectors.

This specification is not limited to describing test vector manifests for a single AWS Crypto Tools
product, but each feature will usually only apply to a single product unless otherwise specified.

These test vectors are intended to be used to validate interoperability across implementations
of clients, primarily targeting those clients owned by AWS Crypto Tools.

[For security issue notifications, see CONTRIBUTING.md.](./CONTRIBUTING.md#security-issue-notifications)

# Specification Structure

A specification is defined as the combination of all features. Each feature is defined in a separate
file in the [features directory](features/FEATURES.md).

In this specification, each feature will generally describe a single test vector manifest definition.

# Glossary

-   **Test Vector** : Information about a single test case. Used to either process existing data
    or create new data.
-   **Test Vector Manifest** : A document that describes one or more test vectors.
-   **Feature** : A self-contained set of behavior that is defined as part of a specification.
    For this specification, these will usually be definitions of test vector manifests.
-   **Specification** : A collection of one or more features that in summary define a standard
    set of behaviors and/or data formats.
