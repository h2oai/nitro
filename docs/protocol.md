# Protocol

This page describes the protocol used by the Nitro client to communicate with servers.

### Audience

This information is intended for developers working on providing language-specific servers (backends) for Nitro clients.

### Terminology

- **Workflow**: A screen flow sequence supported by the server, also called *wizard*.

## Overview

A client establishes a WebSocket connection with a server.
Thereafter, the client and server communicate using MsgPack-encoded messages.

## Message Types

There are six kinds of messages:

1. `Error`: Sent by the client or server. Describes an error.
2. `Join`: Sent by the client. Describes a request to join the server.
3. `Switch`: Sent by the client. Describes a request to switch to a different workflow.
4. `Input`: Sent by the client. Describes an input to the active workflow.
5. `Output`: Sent by the server. Describes an output from the active workflow, to be displayed on the screen.
6. `Set`: Sent by the server. Describes global configuration settings.

Each message must have a type `t` from `1` to `6`.

## Scenarios

### Client joins server

To join a server, the client sends a `Join` message:

| Name     | Type             | Required? | Description  | 
|----------|------------------|-----------|--------------|
| `t`      | `int=2`          | Y         | Message type |
| `method` | `str`            | N         | Method       |
| `params` | `dict<str, str>` | N         | Parameters   |

The `method` and `params` are derived from the URL hashbang.

Example 1: https://example.com/ yields:

```yaml
t: 2
```

Example 2: https://example.com/#!foo?bar=qux&baz=42 yields:

```yaml
t: 2
method: "foo"
params:
  bar: "qux"
  baz: "42"
```

The server is expected to interpret `method` as the name of the initial workflow.
If `method`  is empty, the server is expected to launch the default workflow,
typically one that displays the home page or landing page.

### Server accepts client

The server responds to the `Join` message with a `Set` message:

| Name       | Type    | Required? | Description  | 
|------------|---------|-----------|--------------|
| `t`        | `int=6` | Y         | Message type |
| `settings` | `dict`  | Y         | `Settings`   |

The `settings` attribute holds configuration settings, described in
[protocol.ts](https://github.com/h2oai/nitro/blob/main/web/src/protocol.ts).

### Server sends output

The server immediately follows up the `Set` message with a `Output` message from the workflow corresponding
to the `method` sent in the `Join` message:

| Name   | Type    | Required? | Description    | 
|--------|---------|-----------|----------------|
| `t`    | `int=5` | Y         | Message type   |
| `xid`  | `str`   | Y         | Correlation ID |
| `box`  | `dict`  | Y         | `Box`          |
| `edit` | `dict`  | N         | `Edit`         |

The correlation ID `xid` is expected to be unique per message at the connection (WebSocket) level.

The `box` and `edit` attributes hold the view's root box and the kind of modification respectively,
described in [protocol.ts](https://github.com/h2oai/nitro/blob/main/web/src/protocol.ts).

Each `Box` (and each nested `Box`) in the UI is expected to have a unique correlation ID `xid`.

If `edit` is missing, the `box` overwrites the entire UI. This is the common case.

### Client sends input

When the user provides input, the client sends an `Input` message:

| Name     | Type           | Required? | Description    | 
|----------|----------------|-----------|----------------|
| `t`      | `int=4`        | Y         | Message type   |
| `xid`    | `str`          | Y         | Correlation ID |
| `inputs` | `array<Input>` | Y         | `Input` array  |

The correlation ID `xid` will match the one on the `Output` message sent by the server.
Note that unlike typical client/server applications where the client makes the request,
and the server replies with a response, the roles in Nitro are reversed: the server makes
a request using an `Output` message, and the client responds with an `Input` message.
Therefore, the correlation ID of the `Input` will match that of the `Output`, not the other way around.

The `Input` array holds the user's inputs. Each `Input` is a `[xid, value]` pair (or tuple).
The `xid` in the pair corresponds to that of the `Box` that produced the `value`.

The server is expected to hand back the input values to the call site, using the correlation id `xid`
to ensure that the call site can destructure and process the values in the correct order.

### Client switches workflow

When the user switches to a different workflow (through the menu or nav or address bar),
the client sends a `Switch` message:

| Name     | Type             | Required? | Description  | 
|----------|------------------|-----------|--------------|
| `t`      | `int=2`          | Y         | Message type |
| `method` | `str`            | N         | Method       |
| `params` | `dict<str, str>` | N         | Parameters   |

The `method` and `params` are derived from the URL hashbang, exactly similar to the `Join` message.

The server is expected to interpret `method` as the name of workflow to switch to.
If `method`  is empty, the server is expected to launch the default workflow,
typically one that displays the home page or landing page.

### Errors

If either the client or server run into an unexpected or error condition, they produce an `Error` message:

| Name   | Type    | Required? | Description  | 
|--------|---------|-----------|--------------|
| `t`    | `int=1` | Y         | Message type |
| `code` | `int`   | Y         | Error code   |
| `text` | `str`   | Y         | Error text   |
