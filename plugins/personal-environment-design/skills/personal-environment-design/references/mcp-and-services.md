# MCP and services

Choose transport, process lifetime, and execution location together to supply
the required capability without unnecessary work or maintenance. Inspect the
actual client, server, authentication, and implementation support. An HTTP URL
alone does not establish a compatible MCP service or a remotely hosted backend.

## Prefer compatible direct connections

When the client and a remote MCP server support a suitable native Streamable
HTTP connection, use it instead of an unnecessary local bridge. Check their
actual protocol and authentication support against current documentation and
a representative call. A bridge remains useful when a concrete compatibility
need justifies it; changing transport labels is not itself an improvement.

## Choose where execution belongs

For capabilities that do not require the recipient's local files, devices,
applications, or desktop, compare suitable existing hosted services with local
execution. Prefer an available hosted route when its functions, authentication,
data boundaries, reliability, and cost fit the task. Verify where the backend
actually executes: a cloud entrypoint or tunnel can still launch work locally.
A remote API is not itself a hosted MCP implementation.

Use existing compatible capabilities before recreating an adapter. New hosting
infrastructure earns its setup and maintenance through the actual need, rather
than through a preference for a cloud label.

## Share local work where state permits it

If execution must remain local, consider a shared service when repeated instances
create meaningful overhead. Prefer native Streamable HTTP support when it fits
the client and server; a small adapter may be justified to supply missing sharing
support. Bind a local-only service to the appropriate local interface.

Check separation of work directories, mutable task state, credentials,
permissions, cancellation, and lifecycle for the actual concurrent consumers.
A transport session identifier alone does not establish task isolation. Share
only what can safely be shared, retaining task-specific state or separate
instances where needed.

Inspect the expensive execution layer, including child processes. One listener
that still launches a heavy backend for every conversation may retain the
duplication that motivated the change. Connection sharing and backend sharing
are different achievements.

## Match effort to observed cost

Measure runtime memory, repeated instance counts, lifetime, startup and call
latency, and relevant service charges. Compare the aggregate cost with migration
and ongoing maintenance. Distinguish running memory from download size or disk
footprint. Many small replicas can matter more than one larger service.

Investigate substantial avoidable duplication and implement a suitable shared
or hosted route when compatibility, isolation, and expected savings justify it.
Low aggregate overhead or disproportionate implementation cost can justify
retaining a working stdio arrangement. Concrete compatibility or state-isolation
needs can also justify separate instances. Existing configuration alone does
not settle the choice, and a transport preference does not justify losing a
needed capability or boundary.

## Verify the successor and retire displaced routes

Exercise the actual client with representative operations. If sharing affects
mutable state, use independent task contexts to check the relevant boundaries,
including cancellation where it can affect another consumer. Observe process
counts and resource use under relevant concurrency before claiming savings.
Verify remote execution before claiming local work has been removed.

Use checks proportional to the changed behavior and its consequences. After
successor readback, remove obsolete bridges, duplicate launch entries, and unused
registrations through their maintained owners. Preserve routes with current
consumers. Keep credentials, service management, source configuration, and
runtime delivery with their actual owners and existing authorization.
