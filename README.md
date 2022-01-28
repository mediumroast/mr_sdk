## Mediumroast Solutions Development Kit Description
**Axiom: Data stored in any software is clearly owned by the user and not the provider/developer.**

Therefore, all steps must be taken to make this axiom plain and clear to the user, provided the steps do not damage the function and core behaviors of the software.  As people who grew up in companies that practiced this axiom we believe that all steps include at least the following and likely more: 
- Open APIs both core and helper operations, 
- Open SDKs that realize the operation of the API,
- Access to as much as as can be stored in the database,
- Open approaches to backup and restore packages.
- Externalized data should be self explainable.

In the space we're intending for the mediumroast.io, we see SaaS products missing external APIs, having APIs that are slow to surface, APIs gated behind a paywall, or altogether incomplete.  This situation is frustrating to the user and the developer alike, and a barrier to realizing a healthy and vibrant ecosystem.  So, to that end we're releasing, as a part of our open alpha drive, our internal APIs we're actively developing against.  Our intentions are to enable users and developers to play with the software using a variety of interfaces.  Our initial releases include both Python and Javascript SDKs covering ETL into the system plus the APIs for the backend consumed by Caffeine, our Machine Intelligence service, and our CLIs and Web UI.

## Python
A Python package wrapping the backend Mediumroast API, providing ETL APIs to enable interacting between the Mediumroast and key source systems like S3/Minio, and several Command Line Interface examples to exercise the APIs.  Initially this set of tools enables users to capture metadata from a source system, create, read, update and delete data in the backend.  Information on the installation of the package and basic function of the CLIs can be found in the [README.md](https://github.com/mediumroast/mr_sdk/tree/main/python).

## Javascript
A Node.js Javascript package wrapping the backend Mediumroast API including several Command Line Interface examples to exercise the APIs.  This tool set will eventually be the basis for production Command Line Interfaces and Text User Interfaces for the mediumroast.io.  Additionally we will be using this SDK as the basis of our Web User Interface moving forward. Information on the installation of the package and basic function of the CLIs can be found in the [README.md](https://github.com/mediumroast/mr_sdk/tree/main/javascript).

## Future work
At present the mediumroast.io is entering what we are calling an open alpha so stay tuned as we get things up and running.  Already Caffeine is proving to be quite helpful for us in Product Management discovery consulting. Essentially, it is taking a process for us that would usually be days down to hours.  We're obviously going to do more and these SDKs are key to that, but this early release is just the start of our journey.  Along the path the things we expect to do with these SDKs include but is not limited to the following.
1. Separate out the Python and Javascript SDKs into discrete packages that can be pushed to PyPi and NPM.
2. Make the CLI complete, production quality and also a separate package.
3. Obviously improve the documentation with examples, samples, and working programs.