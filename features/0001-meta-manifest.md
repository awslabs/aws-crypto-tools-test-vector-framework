
|           |                                               |
|:----------|:----------------------------------------------|
|__Feature__|Meta Manifest                                  |
|__Version__|1                                              |
|__Created__|2018-06-21                                     |
|__Updated__|ISO-8601 date feature was most recently updated|

## Summary

The meta-manifest is a file identifying one or more additional manifests, along with indicating 
the type of each manifest.

## Out of Scope

This is not a definition of any other manifest types.

## Motivation

It is helpful to have a single entry point for all test vectors. Every manifest contains sufficient 
information for a client to use it with no additional information, but the meta-manifest provides 
a single reference point for all manifests within a given test set.

## Drawbacks

What problems were introduced by this feature, or what gaps in the original problems does
it leave open?

## Guide-level Explanation

The meta-manifest is a JSON document that identifies the location and type of one or more test 
case manifests. It is used to enumerate all manifests to use for a given test set. Each manifest 
is identified by type and a URI is specified from which the manifest can be obtained.

## Reference-level Explanation

### Contents

#### manifest

Map identifying this manifest.

* `type` : Identifies this manifest as a meta-manifest.
    * Must be `meta`
* `version` : Identifies the version of this document that describes the contents of the manifest.

#### tests

List of references to additional manifest.

Each reference must contain:
* `manifest` : URI that maps to a valid manifest.
* `type` : Type identifier for the specified manifest.
    * This must be the `type` value for the manifest in question.

### Example

```json
{
    "manifest": {
        "type": "meta",
        "version": 1
    },
    "tests": [
        {
            "manifest": "file://relative/file/path.json",
            "type": "decrypt"
        },
        {
            "manifest": "s3://example/key/path.json",
            "type": "serialize"
        },
        {
            "manifest": "https://example.com/manifests/example.json",
            "type": "deserialize"
        }
    ]
}
```
