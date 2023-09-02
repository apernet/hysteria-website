# Full Server Config

This page provides documentation for every field in the server configuration file.

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

## Listen

The `listen` field is the server's listen address. If omitted, the server will listen on `:443' since that's the default HTTP/3 port.

```yaml
listen: :443 # (1)!
```

1. When the IP address is omitted, the server will listen on all interfaces.

## TLS

You can have either `tls` or `acme`, but not both.

=== "TLS"

    ```yaml
    tls:
      cert: some.crt
      key: some.key
    ```

=== "ACME"

    ```yaml
    acme:
      domains:
        - domain1.com
        - domain2.org
      email: your@email.net
      ca: zerossl # (1)!
      disableHTTP: false # (2)!
      disableTLSALPN: false # (3)!
      altHTTPPort: 8080 # (4)!
      altTLSALPNPort: 4443 # (5)!
      dir: my_acme_dir # (6)!

    ```

    1. The CA to use. Can be `letsencrypt` or `zerossl`.
    2. Disable HTTP challenge.
    3. Disable TLS-ALPN challenge.
    4. Alternate HTTP challenge port.
    5. Alternate TLS-ALPN challenge port.
    6. The directory to store the ACME account key and certificates.

## Obfuscation

By default, the Hysteria protocol mimics HTTP/3. If your network specifically blocks QUIC or HTTP/3 traffic (but not UDP in general), obfuscation can be used to work around this. We currently have an obfuscation implementation called "Salamander" that converts packets into seamingly random bytes with no pattern. This feature requires a password that must be identical on both the client and server sides.

> **NOTE:** Enabling obfuscation will make your server incompatible with standard QUIC connections and it will no longer function as a valid HTTP/3 server.

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
  maxIncomingStreams: 1024 # (6)!
  disablePathMTUDiscovery: false # (7)!
```

1. The initial QUIC stream receive window size.
2. The maximum QUIC stream receive window size.
3. The initial QUIC connection receive window size.
4. The maximum QUIC connection receive window size.
5. The maximum idle timeout. How long the server will consider the client still connected without any activity.
6. The maximum number of concurrent incoming streams.
7. Disable QUIC path MTU discovery.

The default stream and connection receive window sizes are 8MB and 20MB, respectively. **We do not recommend changing these values unless you fully understand what you are doing.** If you choose to change these values, we recommend keeping the ratio of stream receive window to connection receive window at 2:5.

## Bandwidth

```yaml
bandwidth:
  up: 1 gbps
  down: 1 gbps
```

The bandwidth values on the server side act as speed limits, limiting the maximum rate at which the server will send and receive data (per client). **Note that the server's upload speed is the client's download speed, and vice versa.** You can omit these values or set them to zero on either or both sides, which would mean no limit.

Supported units are:

- `bps` or `b` (bits per second)
- `kbps` or `kb` or `k` (kilobits per second)
- `mbps` or `mb` or `m` (megabits per second)
- `gbps` or `gb` or `g` (gigabits per second)
- `tbps` or `tb` or `t` (terabits per second)

### Ignore client bandwidth

```yaml
ignoreClientBandwidth: false
```

`ignoreClientBandwidth` is a special option that, when enabled, makes the server to disregard any bandwidth hints set by clients, opting to use a more traditional congestion control algorithm (currently BBR) instead. This effectively overrides any bandwidth values set by clients in both directions.

This feature is primarily useful for server owners who prefer congestion fairness over other network traffic, or who do not trust users to accurately set their own bandwidth values.

## UDP

```yaml
disableUDP: false
```

`disableUDP` disables UDP forwarding, only allowing TCP connections.

```yaml
udpIdleTimeout: 60s
```

`udpIdleTimeout` specifies the amount of time the server will keep a local UDP port open for each UDP session that has no activity. This is conceptually similar to the NAT UDP session timeout.

## Authentication

```yaml
auth:
  type: password
  password: your_password # (1)!
  userpass: # (2)!
    user1: pass1
    user2: pass2
    user3: pass3
  http:
    url: http://your.backend.com/auth # (3)!
    insecure: false # (4)!
  command: /etc/some_command # (5)!
```

1. Replace with a strong password of your choice.
2. A map of username-password pairs.
3. The URL of the backend server that handles authentication.
4. Disable TLS verification for the backend server (only applies to HTTPS URLs).
5. The path to the command that handles authentication.

### HTTP authentication

When using HTTP authentication, the server will send a `POST` request to the backend server with the following JSON body when a client attempts to connect:

```json
{
  "addr": "123.123.123.123:44556", // (1)!
  "auth": "something_something", // (2)!
  "tx": 123456 // (3)!
}
```

1. The client's IP address and port.
2. The client's authentication payload.
3. The tx rate (in bytes per second) the client requested.

Your endpoint must respond with a JSON object with the following fields:

```json
{
  "ok": true, // (1)!
  "id": "john_doe" // (2)!
}
```

1. Whether to allow this client to connect.
2. The client's unique identifier. This is used in logs and traffic statistics API.

> **NOTE:** The HTTP status code must be 200 for the authentication to be considered successful.

### Command authentication

When using command authentication, the server will execute the specified command with the following arguments when a client attempts to connect:

```bash
/etc/some_command addr auth tx # (1)!
```

1. The definition of each argument is the same as in the HTTP authentication section above.

The command must print the client's unique identifier to `stdout` and return with exit code 0 if the client is allowed to connect, or return with a non-zero exit code if the client is rejected.

If the command fails to execute, the client will be rejected.

## Resolver

You can specify what resolver (DNS server) to use to resolve domain names in client requests.

```yaml
resolver:
  type: udp
  tcp:
    addr: 8.8.8.8:53 # (1)!
    timeout: 4s # (2)!
  udp:
    addr: 8.8.4.4:53 # (3)!
    timeout: 4s
  tls:
    addr: 1.1.1.1:853 # (4)!
    timeout: 10s
    sni: cloudflare-dns.com # (5)!
    insecure: false # (6)!
  https:
    addr: 1.1.1.1:443 # (7)!
    timeout: 10s
    sni: cloudflare-dns.com
    insecure: false
```

1. The address of the TCP resolver.
2. The timeout for DNS queries.
3. The address of the UDP resolver.
4. The address of the TLS resolver.
5. The SNI to use for the TLS resolver.
6. Disable TLS verification for the TLS resolver.
7. The address of the HTTPS resolver.

If omitted, Hysteria will use the system's default resolver.

## ACL

ACL, often used in combination with outbounds, is a very powerful feature of the Hysteria server that allows you to customize the way client's requests are handled. For example, you can use ACL to block certain addresses, or to use different outbounds for different websites.

For details on syntax, usage and other information, please refer to the [ACL documentation](ACL.md).

You can have either `file` or `inline`, but not both.

=== "File"

    ```yaml
    acl:
      file: some.txt # (1)!
      # geoip: GeoLite2-Country.mmdb (2)
    ```

    1. The path to the ACL file.
    2. Optional. The path to the GeoIP database file. **Hysteria will automatically download the latest database if this field is omitted.**

=== "Inline"

    ```yaml
    acl:
      inline: # (1)!
        - reject(v2ex.com)
        - reject(*.v2ex.com)
        - reject(all, udp/443)
        - reject(geoip:cn)
      # geoip: GeoLite2-Country.mmdb (2)
    ```

    1. The list of inline ACL rules.
    2. Optional. The path to the GeoIP database file. **Hysteria will automatically download the latest database if this field is omitted.**

> **NOTE:** Hysteria only supports MaxMind's GeoLite2 Country database in MMDB format for GeoIP functionality. If you don't know how to get the right file, omit the geoip field and let Hysteria automatically download the latest version. The database file will only be downloaded if there is at least one GeoIP rule in the ACL.

## Outbounds

Outbounds are used to define the "exit" through which a connection should be routed. For example, when [combined with ACL](ACL.md), you can route all traffic except Netflix directly through the local interface, while routing Netflix traffic through a SOCKS5 proxy.

Currently, Hysteria supports the following outbound types:

- `direct`: Direct connection through the local interface.
- `socks5`: SOCKS5 proxy.

**If you do not use ACL, all connections will always be routed through the first ("default") outbound in the list, and all other outbounds will be ignored.**

```yaml
outbounds:
  - name: my_outbound_1 # (1)!
    type: direct
  - name: my_outbound_2
    type: socks5
    socks5:
      addr: shady.proxy.ru:1080 # (2)!
      username: hackerman # (3)!
      password: Elliot Alderson # (4)!
```

1. The name of the outbound. This is used in ACL rules.
2. The address of the SOCKS5 proxy.
3. Optional. The username for the SOCKS5 proxy, if authentication is required.
4. Optional. The password for the SOCKS5 proxy, if authentication is required.

### Customizing `direct` outbound

The direct outbound has a few additional options that can be used to customize its behavior:

> **NOTE:** The options `bindIPv4`, `bindIPv6`, and `bindDevice` are mutually exclusive. You can either specify `bindIPv4` and/or `bindIPv6` without `bindDevice`, or use `bindDevice` without `bindIPv4` and `bindIPv6`.

```yaml
outbounds:
  - name: hoho
    type: direct
    direct:
      mode: auto # (1)!
      bindIPv4: 2.4.6.8 # (2)!
      bindIPv6: 0:0:0:0:0:ffff:0204:0608 # (3)!
      bindDevice: eth233 # (4)!
```

1. See the explanation below.
2. The local IPv4 address to bind to.
3. The local IPv6 address to bind to.
4. The local network interface to bind to.

The available `mode` values are:

- `auto`: Default. Dual-stack "happy eyeballs" mode. The client will attempt to connect to the destination using both IPv4 and IPv6 addresses (if available), and use the first one that succeeds.
- `64`: Always use IPv6 if available, otherwise use IPv4.
- `46`: Always use IPv4 if available, otherwise use IPv6.
- `6`: Always use IPv6. Fail if no IPv6 address is available.
- `4`: Always use IPv4. Fail if no IPv4 address is available.

## Traffic Stats API (HTTP)

The Traffic Stats API allows you to query the server's traffic statistics and kick clients using an HTTP API. For endpoints and usage, please refer to the [Traffic Stats API documentation](Traffic-Stats-API.md).

> **NOTE:** This API has no authentication, so you should not expose it to the public Internet. We also recommend blocking it with ACL to prevent clients from accessing it.

```yaml
trafficStats:
  listen: :9999 # (1)!
```

1. The address to listen on.

## Masquerade

One of the keys to Hysteria's censorship resistance is its ability to masquerade as standard HTTP/3 traffic. This means that not only do the packets appear as HTTP/3 to middleboxes, but the server also responds to HTTP requests like a regular web server. However, this means that your server must actually serve some content to make it appear authentic to potential censors.

**If censorship is not a concern, you can omit the `masquerade` section entirely. In this case, Hysteria will always return "404 Not Found" for all HTTP requests.**

Currently, Hysteria provides the following masquerade modes:

- `file`: Act as a static file server, serving files from a directory.
- `proxy`: Act as a reverse proxy, serving content from another website.

```yaml
masquerade:
  type: proxy
  file:
    dir: /www/masq # (1)!
  proxy:
    url: https://some.site.net # (2)!
    rewriteHost: true # (3)!
```

1. The directory to serve files from.
2. The URL of the website to proxy.
3. Whether to rewrite the `Host` header to match the proxied website. This is required if the target web server uses `Host` to determine which site to serve.

You can test your masquerade configuration by starting Chrome with a special flag (to force QUIC):

```bash
chrome --origin-to-force-quic-on=your.site.com:443 # (1)!
```

1. Replace with the domain name of your server.

Then visit `https://your.site.com` to verify that it works as expected.
