# IxSuiteStore

IxSuiteStore exposes a REST API to facilitate automation of its features via scripting.
The REST API provided by IxSuiteStore follows the Ixia REST API v1 standard. In addition to the normal
CRUD operations available via the HTTP POST, GET, PATCH, and DELETE methods, respectively, the
standard defines a mechanism for invoking long-running operations (a.k.a. Async operations). These
operations can be initiated with a POST which then returns an URL by which the status of the operation
can be polled. In IxSuiteStore, all methods are invoked by this Async operation mechanism. Most methods
will return a result of SUCCESS, ERROR, or EXCEPTION right away, but any asynchronous operation call
may return an IN_PROGRESS result and require polling the accompanying status URL until the result is
available.

For more details, please review the IxSuiteStoreUserGuide.pdf included in the IxSuiteStore app.