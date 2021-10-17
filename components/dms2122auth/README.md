# DMS 2021-2022 Authentication Service

This service provides authentication functionalities to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
# Initialize the administrator user admin (password: admin)
dms2122auth-create-admin
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2122auth/config.yml`. This path is thus usually `${HOME}/.config/dms2122auth/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `service_host` (mandatory): The service host.
- `service_port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.
- `jws_secret`: The secret to cypher the JWS tokens.
- `jws_ttl`: The number of seconds before the JWS tokens are invalidated.
- `authorized_api_keys`: An array of keys (in string format) that integrated applications should provide to be granted access to certain REST operations.

## Running the service

Just run `dms2122auth` as any other program.

## REST API specification

This service exposes a REST API in OpenAPI format that can be browsed at `dms2122auth/openapi/spec.yml` or in the HTTP path `/api/v1/ui/` of the service.

## Services integration

The authentication service requires an API key to ensure that only the whitelisted clients can operate through the REST API.

Requesting clients must include their own, unique API key in the `X-ApiKey-Auth` header.

When a request under that security schema receives a request, the key in this header is searched in the whitelisted API keys at the service configuration (in the `authorized_api_keys` entry). If the header is not included or the key is not in the whitelist, the request will be immediately rejected, before being further processed.

## Authentication workflow

Most operations against this service will require a user session to be opened. These sessions are passed in the requests through a signed token (JWS).

First, a user presents their credentials to the authorization operation `POST /auth`, passed in the `Authorization` header as basic HTTP authorization (base64-encoded `username:password`).

If the credentials are accepted as valid once compared to the stored user credentials, a JWS token with basic user information is generated and returned as the response. Clients must store this token, as will be required by most other operations to ensure it is a legitimate user.

When the token duration expires, is altered, or lost, the authorization cycle must start again. Requesting a token using an existing one will generate a new token. Thus clients can refresh these sessions as long as the application is being used.
