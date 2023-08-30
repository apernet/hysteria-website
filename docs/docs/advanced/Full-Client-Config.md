# Full Client Config

This page provides documentation for every field in the client configuration file.

> **NOTE:** One common pattern you'll encounter in both the client & server configurations is the "type selector":

```yaml
example:
  type: a
  a:
    something: something
  b:
    something: something
  c:
    something: something
```

`type` determines which mode to use and which subfields to parse. In this example, the `example` field can be either `a`, `b` or `c`. If `a` is selected, the `a` subfield will be parsed and the `b` and `c` subfields will be ignored.

## Server address

The `server` field specifies the address of the Hysteria server that the client should connect to. The address can be formatted as either `host:port` or just `host`. If the port is omitted, it defaults to 443.

You also have the option to use a Hysteria 2 URI (`hysteria2://`). In this case, because the URI already includes the password and certain other settings, you don't (and can't) specify them separately in the configuration file.

=== "Address"

    ```yaml
    server: example.com
    ```

=== "URI"

    ```yaml
    server: hysteria2://user:pass@example.com/
    ```

## Authentication

```yaml
auth: some_password
```

> **NOTE:** If the server uses the `userpass` authentication, the format must be `username:password`.

## TLS

```yaml
tls:
  sni: another.example.com # (1)!
  insecure: false # (2)!
  pinSHA256: BA:88:45:17:A1... # (3)!
  ca: custom_ca.crt # (4)!
```

1. Server name to use for TLS verification. If omitted, the server name will be extracted from the `server` field.
2. Disable TLS verification.
3. Verify the server's certificate fingerprint. You can obtain the fingerprint of your certificate using openssl: `openssl x509 -noout -fingerprint -sha256 -in your_cert.crt`
4. Use a custom CA certificate for TLS verification.

## Obfuscation

By default, the Hysteria protocol mimics HTTP/3. If your network specifically blocks QUIC or HTTP/3 traffic (but not UDP in general), obfuscation can be used to work around this. We currently have an obfuscation implementation called "Salamander" that converts packets into seamingly random bytes with no pattern. This feature requires a password that must be identical on both the client and server sides.

> **NOTE:** Using an incorrect obfuscation password will result in a connection timeout, just as if the server were not running at all. If you experience connection problems, double-check that the password is correct.

```yaml
obfs:
  type: salamander
  salamander:
    password: cry_me_a_r1ver # (1)!
```

1. Replace with a strong password of your choice.

## QUIC parameters

```yaml
quic:
  initStreamReceiveWindow: 8388608 # (1)!
  maxStreamReceiveWindow: 8388608 # (2)!
  initConnReceiveWindow: 20971520 # (3)!
  maxConnReceiveWindow: 20971520 # (4)!
  maxIdleTimeout: 30s # (5)!
  keepAlivePeriod: 10s # (6)!
  disablePathMTUDiscovery: false # (7)!
```

1. The initial QUIC stream receive window size.
2. The maximum QUIC stream receive window size.
3. The initial QUIC connection receive window size.
4. The maximum QUIC connection receive window size.
5. The maximum idle timeout. How long until the client will consider the connection dead if no packets from the server are received.
6. The keep-alive period. How often the client will send a packet to the server to keep the connection alive.
7. Disable QUIC path MTU discovery.

The default stream and connection receive window sizes are 8MB and 20MB, respectively. **We do not recommend changing these values unless you fully understand what you are doing.** If you choose to change these values, we recommend keeping the ratio of stream receive window to connection receive window at 2:5.

## Bandwidth

```yaml
bandwidth:
  up: 100 mbps
  down: 200 mbps
```

**Set the `up` and `down` bandwidth values to match the maximum rates of your current Internet connection.** Although highly recommended, these settings are optional. If you're unsure about the bandwidth on one or both sides, you can either set only one side or remove this bandwidth section entirely.

The client's actual upload speed will be the lesser of the value specified here and the server's maximum download speed (if set by the server). Similarly, the client's actual download speed will be the lesser of the value specified here and the server's maximum upload speed (if set by the server).

One exception is that if the server has enabled the `ignoreClientBandwidth` option, the values specified here will be ignored.

Supported units are:

- `bps` or `b` (bits per second)
- `kbps` or `kb` or `k` (kilobits per second)
- `mbps` or `mb` or `m` (megabits per second)
- `gbps` or `gb` or `g` (gigabits per second)
- `tbps` or `tb` or `t` (terabits per second)

## Fast Open

Fast Open can shave one roundtrip time (RTT) off each connection, but at the cost of the correct semantics of SOCKS5/HTTP proxy protocols. When this is enabled, the client always immediately accepts a connection without confirming with the server that the destination is reachable. If the server then fails or rejects the connection, the client will simply close the connection without sending any data back to the proxy client.

```yaml
fastOpen: true
```

## Lazy

When enabled, the client is "lazy" in the sense that it will only attempt to connect to the server if there is an incoming connection from one of the enabled client modes. This differs from the default behavior, where the client attempts to connect to the server as soon as it starts up.

The `lazy` option can be useful if you're unsure when you'll use the client and want to avoid idle connections. It's also useful if your Internet connection might not be ready when you start the Hysteria client.

```yaml
lazy: true
```

## Modes

To use the Hysteria client, you must at least specify one of the following modes:

### SOCKS5

A SOCKS5 proxy server that can be used with any SOCKS5-compatible application. Supports both TCP and UDP.

```yaml
socks5:
  listen: 127.0.0.1:1080 # (1)!
  username: user # (2)!
  password: pass # (3)!
  disableUDP: false # (4)!
```

1. The address to listen on.
2. Optional. The username to require for authentication.
3. Optional. The password to require for authentication.
4. Optional. Disable UDP support.

### HTTP

An HTTP proxy server that can be used with any HTTP proxy-compatible application. Supports both plaintext HTTP and HTTPS (CONNECT).

```yaml
http:
  listen: 127.0.0.1:8080 # (1)!
  username: king # (2)!
  password: kong # (3)!
  realm: martian # (4)!
```

1. The address to listen on.
2. Optional. The username to require for authentication.
3. Optional. The password to require for authentication.
4. Optional. The realm to require for authentication.

### TCP Forwarding

TCP Forwarding allows you to forward one or more TCP ports from the server (or any remote host) to the client. This is useful, for example, if you want to access a service that is only available on the server's network.

```yaml
tcpForwarding:
  - listen: 127.0.0.1:6600 # (1)!
    remote: 127.0.0.1:6600 # (2)!
  - listen: 127.0.0.1:6601 # (3)!
    remote: other.machine.internal:6601
```

1. The address to listen on.
2. The address to forward to.
3. You can have one or more forwarding rules.

### UDP Forwarding

UDP Forwarding allows you to forward one or more UDP ports from the server (or any remote host) to the client. This is useful, for example, if you want to access a service that is only available on the server's network.

```yaml
udpForwarding:
  - listen: 127.0.0.1:5300 # (1)!
    remote: 127.0.0.1:5300 # (2)!
    timeout: 20s # (3)!
  - listen: 127.0.0.1:5301 # (4)!
    remote: other.machine.internal:5301
    timeout: 20s
```

1. The address to listen on.
2. The address to forward to.
3. Optional. The timeout for each UDP session. If omitted, the default timeout is 60 seconds.
4. You can have one or more forwarding rules.

### TCP TProxy (Linux only)

TPROXY (transparent proxy) is a Linux-specific feature that allows you to transparently proxy TCP connections. For information, please refer to [Setting up TPROXY](TPROXY.md).

```yaml
tcpTProxy:
  listen: 127.0.0.1:2500 # (1)!
```

1. The address to listen on.

### UDP TProxy (Linux only)

TPROXY (transparent proxy) is a Linux-specific feature that allows you to transparently proxy UDP connections. For information, please refer to [Setting up TPROXY](TPROXY.md).

```yaml
udpTProxy:
  listen: 127.0.0.1:2500 # (1)!
  timeout: 20s # (2)!
```

1. The address to listen on.
2. Optional. The timeout for each UDP session. If omitted, the default timeout is 60 seconds.
