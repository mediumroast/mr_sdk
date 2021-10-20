## Mediumroast Solutions Development Kit Description
**Axiom: Data stored in any software is clearly owned by the user and not the provider/developer.**

Therefore, all steps must be taken to make this axiom plain and clear to the user, provided the steps do not damage the function and core behaviors of the software.  As people who grew up in companies that practiced this axiom we believe that all steps include at least the following and likely more: 
- Open APIs both core and helper operations, 
- Open SDKs that realize the operation of the API,
- Access to as much as as can be stored in the database,
- Open approaches to backup and restore packages.
- Externalized data should be self explainable.

In the space we're intending for the mediumroast.io, we see SaaS products missing external APIs, having APIs that are slow to surface, APIs gated behind a paywall, or altogether incomplete.  This situation is frustrating to the user and the developer alike, and a barrier to realizing a healthy and vibrant ecosystem.  So, to that end we're releasing, as a part of our open alpha drive, our internal APIs we're actively developing against.  Our intentions are to enable users and developers  to play with the software using a variety of interfaces.  Our initial release is a Python based SDK, see below, covering ETL, Extract Transform Load, operations and the core API for the backend that our Machine Intelligence service, we're calling it Caffeine, uses.

## Python
A Python package wrapping the backend Mediumroast API, providing ETL APIs to enable interacting between the Mediumroast and key source systems like S3/Minio, and several Command Line Interface examples to exercise the APIs.  Initially this set of tools enables users to capture metadata from a source system, create, read, update and delete data in the backend.  Information on the installation of the package and basic function of the CLIs can be found in the [README.md](https://github.com/mediumroast/mr_sdk/tree/main/python).
