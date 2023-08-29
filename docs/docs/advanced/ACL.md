# ACL

ACL, often used in combination with outbounds, is a very powerful feature of the Hysteria server that allows you to customize the way client's requests are handled.

## Syntax

A valid ACL rule must be in one of the following formats:

- `outbound(address)`
- `outbound(address, proto/port)`
- `outbound(address, proto/port, hijack_address)`

### Address types

The `address` field can be one of the following:

- A single IPv4/IPv6 address, e.g. `1.1.1.1` or `2606:4700:4700::1111`
- An IPv4/IPv6 CIDR, e.g. `73.0.0.0/8` or `2001:db8::/32`
- A domain name, e.g. `example.com`
- A domain name with wildcard, e.g. `*.example.com`
- GeoIP country code, e.g. `geoip:cn` or `geoip:us`
- `all` - match all addresses. Usually placed at the end as the default rule for everything else.

### Proto/port

- `tcp` or `tcp/*` - match all TCP ports
- `udp` or `udp/*` - match all UDP ports
- `tcp/80` - match TCP port 80
- `udp/53` - match UDP port 53
- `*/443` - match TCP and UDP port 443
- `*`, `*/*` or omitted - match both protocols and all ports

### Hijack address

When specified, the connection matching this rule will be hijacked to the specified address. The hijack address must be an IPv4/IPv6 address, not a domain name.

## Matching behavior

### Domain and IP matching

When handling domain-based requests, Hysteria first resolves the domain and then attempts to match against both domain and IP rules. **This means that a rule based on an IP address will apply to all connections that ultimately lead to that IP, regardless of whether the client request used an IP address or a domain name.**

### Rule order

The rules are guaranteed to be matched in a top-to-bottom order. The first rule that matches the request will be used. If no rule matches, the default outbound (the first one in the outbounds list) will be used.

## Built-in outbounds

Unless explicitly overridden in the outbounds list, Hysteria comes with the following built-in outbounds:

- `direct` - direct outbound using default configuration (`auto`, no bind)
- `reject` - reject the connection
- `default` - use the first outbound in the outbounds list; if the list is empty, equivalent to `direct`

## Examples

Assume the following outbounds list:

```yaml
outbounds:
  - name: v4_only
    type: direct
    direct:
      mode: 4
  - name: v6_only
    type: direct
    direct:
      mode: 6
  - name: some_proxy
    type: socks5
    socks5:
      addr: ohno.moe:1080
```

```python
# Use the v6_only outbound for Google
v6_only(google.com)
v6_only(*.google.com)

# Use the v4_only outbound for Twitter
v4_only(twitter.com)
v4_only(*.twitter.com)

# Use the some_proxy outbound for ipinfo.io
some_proxy(ipinfo.io)
some_proxy(*.ipinfo.io)

# Block QUIC protocol
reject(all, udp/443)

# Block SMTP protocol
reject(all, tcp/25)

# Block China and North Korea
reject(geoip:cn)
reject(geoip:kp)

# Block some random ranges
reject(73.0.0.0/8)
reject(2601::/20)

# Hijack 8.8.8.8 to 1.1.1.1 and use default (first) outbound
default(8.8.8.8, *, 1.1.1.1)

# Hijack 8.8.4.4 to 1.1.1.1 and use default (first) outbound, but UDP 53 only
default(8.8.4.4, udp/53, 1.1.1.1)

# Direct all other connections
direct(all)
```
