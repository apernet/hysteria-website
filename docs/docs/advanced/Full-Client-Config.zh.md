# 完整客户端配置

本页面提供了关于客户端配置文件中每一个字段的详细说明。

> **注意：** 在客户端和服务端配置中的多处都有 "类型选择" 的配置格式：

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

`type` 用于确定使用哪种模式以及解析哪些子字段。在这个例子中，`example` 字段可以是 `a`、`b` 或 `c`。如果选择了 `a`，则会解析 `a` 子字段，而 `b` 和 `c` 子字段则会被忽略。

## 服务器地址

`server` 字段用于指定客户端应连接到的 Hysteria 服务器地址。地址可以是 `host:port` 或仅 `host`。如果省略端口，默认为 443。

还可以选择使用 Hysteria 2 URI（`hysteria2://`）。在这种情况下，由于 URI 已经包括密码和一些其他设置，就不需要再在配置中单独指定它们。

=== "地址"

    ```yaml
    server: example.com
    ```

=== "URI"

    ```yaml
    server: hysteria2://user:pass@example.com/
    ```

## 验证

```yaml
auth: some_password
```

> **注意：** 如果服务器使用 `userpass` 验证，格式必须是 `username:password`。

## TLS

```yaml
tls:
  sni: another.example.com # (1)!
  insecure: false # (2)!
  pinSHA256: BA:88:45:17:A1... # (3)!
  ca: custom_ca.crt # (4)!
```

1. 用于 TLS 验证的服务器名称。如果省略，服务器名称将从 `server` 字段中提取。
2. 禁用 TLS 验证。
3. 验证服务器的证书指纹。可以通过 openssl 获取证书指纹：`openssl x509 -noout -fingerprint -sha256 -in your_cert.crt`
4. 使用自定义 CA。

## 传输 (Transport)

`transport` 用于自定义 QUIC 连接使用的底层协议。目前唯一可用的类型是 `udp`，保留类型选项是为了将来可能添加的其他类型。

```yaml
transport:
  type: udp
  udp:
    hopInterval: 30s # (1)!
```

1. 端口跳跃间隔。这只在使用多端口地址时才有效。更多信息请参见 [端口跳跃](Port-Hopping.md)。

## 混淆

默认 Hysteria 协议伪装为 HTTP/3。如果你的网络针对性屏蔽了 QUIC 或 HTTP/3 流量（但允许其他 UDP 流量），可以使用混淆来解决此问题。目前有一个名为 "Salamander" 的混淆实现，将数据包混淆成没有特征的 UDP 包。此功能需要一个混淆密码，密码在客户端和服务端必须相同。

> **注意：** 使用错误的混淆密码将导致无法连接，效果如同服务器没有运行一样。如果遇到连接问题，请先仔细检查混淆密码是否正确。

```yaml
obfs:
  type: salamander
  salamander:
    password: cry_me_a_r1ver # (1)!
```

1. 替换为你的混淆密码。

## QUIC 参数

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

1. 初始的 QUIC 流接收窗口大小。
2. 最大的 QUIC 流接收窗口大小。
3. 初始的 QUIC 连接接收窗口大小。
4. 最大的 QUIC 连接接收窗口大小。
5. 最长空闲超时时间。客户端会在多长时间没有收到任何服务端数据后关闭连接。
6. 心跳包发送间隔。客户端会多久发送一次心跳包以保持连接。
7. 禁用 MTU 探测。

默认的流和连接接收窗口大小分别为 8MB 和 20MB。**除非你完全明白自己在做什么，否则不建议修改这些值。**如果要改，建议保持流接收窗口与连接接收窗口的比例为 2:5。

## 带宽

```yaml
bandwidth:
  up: 100 mbps
  down: 200 mbps
```

Hysteria 内置了两套拥塞控制算法（BBR 与 Brutal），**使用哪个由是否提供了带宽值决定。** 如果希望使用 BBR 而不是 Brutal，可以删除整个 `bandwidth` 部分。详细信息请参见 [带宽行为详解](../advanced/Full-Server-Config.md#_6)。

> **⚠️ 警告** 带宽值并非越大越好，请务必不要超过你当前网络环境所能达到的最大带宽。否则只会适得其反，导致网络拥塞，连接不稳定。

客户端的实际上传速度将是这里指定的值，和服务器最大下载速度（如果服务器设置中指定了）中最小的值。同理，客户端的实际下载速度将是这里指定的值，和服务器最大上传速度中最小的值。

一个例外是，如果服务器启用了 `ignoreClientBandwidth` 选项，这里指定的值将被忽略。

支持的单位有：

- `bps` 或 `b`（每秒比特数）
- `kbps` 或 `kb` 或 `k`（每秒千比特）
- `mbps` 或 `mb` 或 `m`（每秒兆比特）
- `gbps` 或 `gb` 或 `g`（每秒吉比特）
- `tbps` 或 `tb` 或 `t`（每秒太比特）

## 快速打开 (Fast Open)

Fast Open 可以减少每个连接建立时一个 RTT，但代价是 SOCKS5/HTTP 等代理协议的正确语义。当这个选项启用时，客户端总是立即接受一个连接，不先与服务器确认目的地是否可达。如果服务器随后返回失败或拒绝连接，客户端将关闭连接。

```yaml
fastOpen: true
```

## 懒狗模式 (Lazy)

启用该选项后，客户端只在有传入连接的时候才会连接到服务器。默认行为是在启动时立即连接到服务器。

这个选项对于启动后可能长时间没有传入连接的情况，或者刚启动时网络不一定可用的情况很有用。

```yaml
lazy: true
```

## 代理模式

要使用 Hysteria 客户端，必须至少指定下面中的一个代理模式。

### SOCKS5

SOCKS5 代理服务器。支持 TCP 和 UDP。

```yaml
socks5:
  listen: 127.0.0.1:1080 # (1)!
  username: user # (2)!
  password: pass # (3)!
  disableUDP: false # (4)!
```

1. 监听地址。
2. 可选。用于验证的用户名。
3. 可选。用于验证的密码。
4. 可选。禁用 UDP 支持。

### HTTP

HTTP 代理服务器。支持 HTTP 和 HTTPS (CONNECT)。

```yaml
http:
  listen: 127.0.0.1:8080 # (1)!
  username: king # (2)!
  password: kong # (3)!
  realm: martian # (4)!
```

1. 监听地址。
2. 可选。用于验证的用户名。
3. 可选。用于验证的密码。
4. 可选。用于验证的域（realm）。

### TCP 转发

TCP 转发允许你从服务器（或任何远程主机）向客户端转发一个或多个 TCP 端口。这在某些情况下很有用，比如访问服务器本地或者内网的服务。

```yaml
tcpForwarding:
  - listen: 127.0.0.1:6600 # (1)!
    remote: 127.0.0.1:6600 # (2)!
  - listen: 127.0.0.1:6601 # (3)!
    remote: other.machine.internal:6601
```

1. 监听地址。
2. 转发地址。
3. 可以有多个转发规则。

### UDP 转发

UDP 转发允许你从服务器（或任何远程主机）向客户端转发一个或多个 UDP 端口。这在某些情况下很有用，比如访问服务器本地或者内网的服务。

```yaml
udpForwarding:
  - listen: 127.0.0.1:5300 # (1)!
    remote: 127.0.0.1:5300 # (2)!
    timeout: 20s # (3)!
  - listen: 127.0.0.1:5301 # (4)!
    remote: other.machine.internal:5301
    timeout: 20s
```

1. 监听地址。
2. 转发地址。
3. 可选。UDP 会话超时时间。如果省略，默认 60 秒。
4. 可以有多个转发规则。

### TCP TProxy (Linux)

TPROXY（透明代理）是一个仅限 Linux 的特性，允许透明代理 TCP 连接。详细信息请参阅 [配置 TPROXY](TPROXY.md)。

```yaml
tcpTProxy:
  listen: :2500 # (1)!
```

1. 监听地址。

### UDP TProxy (Linux)

TPROXY（透明代理）是一个仅限 Linux 的特性，允许透明代理 UDP 连接。详细信息请参阅 [配置 TPROXY](TPROXY.md)。

```yaml
udpTProxy:
  listen: :2500 # (1)!
  timeout: 20s # (2)!
```

1. 监听地址。
2. 可选。UDP 会话超时时间。如果省略，默认 60 秒。

### TCP Redirect (Linux)

REDIRECT 本质上是一种特殊的 DNAT，目标地址是本机。这种方法早于 TPROXY，是实现 TCP 透明代理的一种较旧方式。如果你的内核支持 TPROXY，我们建议使用 TPROXY 来代替 REDIRECT。

```yaml
tcpRedirect:
  listen: :3500
```

示例：

=== "iptables"

    ```bash
    iptables -t nat -N HYSTERIA
    iptables -t nat -A HYSTERIA -d 0.0.0.0/8 -j RETURN
    iptables -t nat -A HYSTERIA -d 10.0.0.0/8 -j RETURN
    iptables -t nat -A HYSTERIA -d 127.0.0.0/8 -j RETURN
    iptables -t nat -A HYSTERIA -d 169.254.0.0/16 -j RETURN
    iptables -t nat -A HYSTERIA -d 172.16.0.0/12 -j RETURN
    iptables -t nat -A HYSTERIA -d 192.168.0.0/16 -j RETURN
    iptables -t nat -A HYSTERIA -d 224.0.0.0/4 -j RETURN
    iptables -t nat -A HYSTERIA -d 240.0.0.0/4 -j RETURN
    iptables -t nat -A HYSTERIA -p tcp -j REDIRECT --to-ports 3500
    iptables -t nat -A OUTPUT -p tcp -j HYSTERIA
    iptables -t nat -A PREROUTING -p tcp -j HYSTERIA

    ip6tables -t nat -N HYSTERIA
    ip6tables -t nat -A HYSTERIA ! -d 2000::/3 -j RETURN
    ip6tables -t nat -A HYSTERIA -p tcp -j REDIRECT --to-ports 3500
    ip6tables -t nat -A OUTPUT -p tcp -j HYSTERIA
    ip6tables -t nat -A PREROUTING -p tcp -j HYSTERIA
    ```

=== "nftables"

    ```nginx
    define HYSTERIA_REDIRECT_PORT=3500
    define BYPASS_IPV4={
        0.0.0.0/8, 10.0.0.0/8, 127.0.0.0/8, 169.254.0.0/16,
        172.16.0.0/12, 192.168.0.0/16, 224.0.0.0/3
    }
    define BYPASS_IPV6={ ::/128 }

    table inet hysteria_redirect {
      chain prerouting {
        type nat hook prerouting priority filter; policy accept;
        meta l4proto tcp counter jump hysteria
      }

      chain output {
        type nat hook output priority filter; policy accept;
        meta l4proto tcp counter jump hysteria
      }

      chain hysteria {
        ip daddr $BYPASS_IPV4 counter return
        ip6 daddr $BYPASS_IPV6 counter return
        ip6 daddr != 2000::/3 counter return
        meta l4proto tcp counter redirect to :$HYSTERIA_REDIRECT_PORT
      }
    }
    ```
