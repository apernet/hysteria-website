# Logging

Hysteria has the following log levels, which you can control with the `HYSTERIA_LOG_LEVEL` environment variable:

- `debug`
- `info` (default)
- `warn`
- `error`

You can also use the `HYSTERIA_LOG_FORMAT` environment variable to control the log format:

- `console` (default)
- `json` (time will be displayed as the Unix epoch in milliseconds)

Hysteria also checks for version updates by default and prints log messages if a newer version is available. To disable this, set `HYSTERIA_DISABLE_UPDATE_CHECK` to 1.
