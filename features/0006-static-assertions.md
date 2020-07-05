
|           |                          |
|:----------|:-------------------------|
|__Feature__|Static Assertions Manifest|
|__Version__|1                         |
|__Created__|2020-07-02                |
|__Updated__|                          |

## Experimental Implementations

This serves as a reference for which implementations support this experimental feature. This
section should be removed once this feature is promoted from experimental status.

Unique implementations required for promotion: 2

| Repository                                                                         | Language | Pull Request                                             |
|------------------------------------------------------------------------------------|----------|----------------------------------------------------------|
| Link to GitHub repository                                                          | Language | Pull request that added support                          |

## Supported Implementations

This serves as a references for which implementations support this feature. A minimum of two supporting implementations
are required for new feature versions.

| Repository                | Language | Feature Version                   | Minimum Version                                    | Pull Request                    |
|---------------------------|----------|-----------------------------------|----------------------------------------------------|---------------------------------|
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |
| Link to GitHub repository | Language | Supported version of this feature | Minimum version that supports this feature version | Pull request that added support |

## Summary

A static assertions manifest identifies a list of requirements that are human-verifiable rather than machine-verifiable.

## Out of Scope

This file does not describe any mechanism
for automatically creating static assertions
in response to changes in a specification.

## Motivation

As outlined [here](0000-framework.md),
test vectors provide a way to validate 
that each implementation of a tool specification
correctly satisfies various requirements.
There are many aspects of a specification,
however,
that are impractical if not impossible to test programmatically. 
For example, 
specifying consistent naming of a concept,
or that a specific concept is NOT implemented.
It is still useful to provide a mechanism 
for maintainers of an implementation 
to acknowledge and align with such requirements.

## Guide-level Explanation

A static assertions manifest is a JSON document 
that identifies one or more manually-validated aspects
of a tool specification. 
It assigns symbols to human-readable descriptions of these aspects,
so that the test vector handler for an implementation
must explicitly assert that the implementation is consistent.

The intended workflow is that the test vectors
for a particular specification
are updated every time a new feature or change
is added to that specification.
When an implementation's test vector client
attempts to validate a new version of the test vectors,
any new static assertions MUST cause a test failure.
The implementation's maintainers MUST then review the linked documentation
and, if required, update the implementation.
They will then update the test vector client
to allow the static assertion to pass.
Clients will likely encode a static list
of verified static assertions.

Note that a similar process would occur
if and when a new kind of manifest
is added to a set of test vectors:
tests would initially fail
due to the unrecognized manifest type.
A single static assertion is equivalent to
a separate manifest type
that is not parameterized with any actual test vector data.

## Reference-level Explanation

### Contents

#### manifest

Map identifying the manifest.

* `type` : Identifies the manifest as a keys manifest.
    * Must be `static-assertions`
* `version` : Identifies the version of this feature document that describes the manifest.

#### assertions

JSON object mapping assertion names to assertion descriptions.

* `specification` : URI identifying the human-readable description of the assertion. This will most often be a link to a feature, specific sub-section, or  pull request in the relevant specification repository.

### Example

```json
{
    "manifest": {
        "type": "static-assertions",
        "version": 1
    },
    "assertions": {
        "aws-kms-not-just-kms": {
            "specification": "https://github.com/awslabs/aws-encryption-sdk-specification/pull/124"
        },
        "no-keyring-traces": {
            "specification": "https://github.com/awslabs/aws-encryption-sdk-specification/pull/105"
        }
    }
}
```
