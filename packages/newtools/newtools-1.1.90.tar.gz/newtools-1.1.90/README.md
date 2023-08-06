# New Tools

&copy; Dativa 2012-2020, all rights reserved. This code is licensed under MIT license. See [license.txt](https://bitbucket.org/dativa4data/newtools/src/master/licence.txt) for details.

---

Provides useful libraries for processing large data sets. 
Developed by the team at [www.dativa.com](https://www.dativa.com) as we find them useful in our projects.

## Installation

Install using PIP by using

```bash
pip install newtools
```

The default install does not include any of the dependent libraries and runtime errors will be raised if the required libraries are not included.

You can install all dependencies as follows:

```bash
pip install newtools[full]
```

## Contents


The key libraries included here are:
* [S3Location](https://bitbucket.org/dativa4data/newtools/src/master/s3_location.md) - provides a version of the string class for creating and managing S3 locations.
* [CachedPep249Query](https://bitbucket.org/dativa4data/newtools/src/master/cached_query.md) and CachedAthenaQuery - provides functionality for caching query results to S3. 

