The AEA framework makes a multitude of tradeoffs.

Here we present an incomplete list of known limitations:

- The AEABuilder checks the consistency of packages at the `add` stage. However, it does not currently check the consistency again at the `load` stage. This means, if a package is tampered with after it is added to the AEABuilder then these inconsistencies might not be detected by the AEABuilder.

- The AEABuilder assumes that packages with public ids of identical author and package name have a matching version. As a result, if a developer uses a package with matching author and package name but different version in the public id, then the AEABuilder will not detect this and simply use the last loaded package.

<br />
