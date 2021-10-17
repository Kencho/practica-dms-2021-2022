# DMS 2021-2022 Backend Service

This service provides backend logic to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2122backend/config.yml`. This path is thus usually `${HOME}/.config/dms2122backend/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `host` (mandatory): The service host.
- `port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.
- `authorized_api_keys`: An array of keys (in string format) that integrated applications should provide to be granted access to certain REST operations.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.
  - `apikey_secret`: The API key this service will use to present itself to the authentication service in the requests that require so. Must be included in the authentication service `authorized_api_keys` whitelist.

## Running the service

Just run `dms2122backend` as any other program.

## REST API specification

This service exposes a REST API in OpenAPI format that can be browsed at `dms2122backend/openapi/spec.yml` or in the HTTP path `/api/v1/ui/` of the service.

## Services integration

The backend service requires an API key to ensure that only the whitelisted clients can operate through the REST API.

Requesting clients must include their own, unique API key in the `X-ApiKey-Backend` header.

When a request under that security schema receives a request, the key in this header is searched in the whitelisted API keys at the service configuration (in the `authorized_api_keys` entry). If the header is not included or the key is not in the whitelist, the request will be immediately rejected, before being further processed.

This service also has its own API key to integrate itself with the authentication service. This key must be thus whitelisted in the authentication service in order to operate.

As some operations required in the authentication service require a user session, clients using this backend must obtain and keep a valid user session token, that will be passed in the requests to this service to authenticate and authorize them.
