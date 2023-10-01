---
title: Changelog
hide:
  - navigation
---

## 2.0.3

> This release contains important fixes and we strongly encourage everyone to upgrade.

- **[Important]** Fixed the problem where when using BBR (either the client doesn't set bandwidth or the server has `ignoreClientBandwidth` enabled), due to a bug in the BBR implementation, it could not accurately determine the bandwidth and send packets much faster than the limit.
- Fixed the problem where ZeroSSL couldn't acquire certificates due to missing EAB.

## 2.0.2

- Fixed connection issues on some devices due to lack of GSO support
- Added HTTP/HTTPS (TCP) masquerade servers
- Added Android builds

## 2.0.1

- Added TCP redirect mode
- Log HTTP requests handled by masquerade (debug level)
- Added environment variable `HYSTERIA_ACME_DIR` to control ACME data directory location

## 2.0.0

This is the first stable release of Hysteria 2. It's almost a complete rewrite of the original Hysteria, with a new protocol, new features, and various improvements.
