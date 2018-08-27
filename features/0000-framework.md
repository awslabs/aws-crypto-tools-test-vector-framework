
|           |                      |
|:----------|:---------------------|
|__Feature__|Test Vector Framework |
|__Version__|1                     |
|__Created__|2018-06-21            |
|__Updated__|2018-08-14            |

## Summary

The AWS Crypto Tools test vector framework creates a mechanism for defining static test
vectors and associated manifests that describe those test vectors.

These test vectors are intended to be used to validate interoperability across implementations
of clients, primarily targeting those clients owned by AWS Crypto Tools.

They will be composed of JSON manifest files that define one or more test cases, including sufficient 
information for a compatible client to process each test case. These manifest files can also 
identify additional resources needed for a given test case. These resources will be identified 
with a URI. If identifying a local file, the URI will be a relative path from the manifest file's 
parent directory to the target file.

Some types of test manifests will define specific test vectors or instructions for generating
specific test vectors rather than instructions for processing existing test vectors. The
definitions for these manifests should include either the desired manifest or a helper tool
that will generate one.

Every manifest type definition must include a unique manifest type name that will be used by
test vector handlers to identify the manifest type.

## Glossary

* **Test Vector** : Information about a single test case. Used to either process existing data
    or create new data.
* **Test Vector Manifest** : A document that describes one or more test vectors.

## Out of Scope

This file is not a definition or description of any specific type of test vector or manifest.

## Motivation

The AWS Crypto Tools team has built several tools that require multiple implementations.
Interoperability between these implementations is critical. To ensure that these implementations
are actually interoperable, we needed to define test vectors that would allow validation
of various aspects of these tools. As we built more tools and required more types of test
vectors, it became evident that there would be value in defining an extensible framework
for defining many different types of test vectors to avoid having to reinvent the wheel
for every client.

## Drawbacks

We will need to write minimal clients in every language with which we want to use these test
vectors to understand the manifests described in subsequent features.

This should represent acceptable overhead: we would need to write some amount of code for each
language to handle the test vectors anyway and this framework lets us define a consistent
way of handling those test vectors while remaining simple to process.
