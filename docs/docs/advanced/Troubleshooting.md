# Troubleshooting

Below is a list of common issues you may encounter while setting up the client or server, along with suggested solutions.

## failed to initialize client (connect error: timeout: no recent network activity)

This error occurs when the client is unable to connect to the server. The most common causes are:

- The server is not running
- The port is blocked by a firewall
- The server is running at a different address or port.
- The server is listening on a network that's inaccessible to the client.
- The domain name is not resolving to the correct IP address.
- Incorrect obfuscation settings

## failed to initialize client (authentication error, HTTP status code: 404)

This error occurs when the client is rejected by the server. The most common causes are:

- The credentials are incorrect
- You connected to the wrong server
- The server has misconfigured authentication settings

## failed to initialize client (connect error: CRYPTO_ERROR 0x12a (local): tls: failed to verify certificate: x509: certificate signed by unknown authority)

This error occurs when the client considers the server's certificate to be invalid. The most common causes are:

- The server is using a self-signed certificate and you have not added it to the client's trusted CA or used the `insecure` option.
- Your system's trusted CA store is missing the CA that signed the server's certificate.
- You are being MITM'd ([man-in-the-middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)) by a third party.

## failed to load server config (invalid config: listen: listen udp :443: bind: permission denied)

This error occurs when the server does not have permission to bind to the specified port. You can do one of the following:

- Run the server as root
- Give the executable the `cap_net_bind_service` capability: `sudo setcap cap_net_bind_service=+ep ./hysteria-linux-amd64-avx`
