# Hysteria 2 协议规范

Hysteria 是一个基于 QUIC 的 TCP 和 UDP 代理，旨在提高速度、安全性和抗审查能力。本文档描述了 2.0.0 版本之后的 Hysteria 协议，有时内部也称为“v4”协议。以下简称为“协议”或“Hysteria 协议”。

## 需求语言

本文档中的关键词“必须”（MUST）、“禁止”（MUST NOT）、“必需”（REQUIRED）、“应”（SHALL）、“不应”（SHALL NOT）、“应当”（SHOULD）、“不应当”（SHOULD NOT）、“推荐”（RECOMMENDED）、“可以”（MAY）和“可选”（OPTIONAL）应按 RFC 2119 中描述的方式解释。[RFC 2119](https://tools.ietf.org/html/rfc2119).

## 底层协议 & Wire Format

Hysteria 协议必须在标准 QUIC 传输协议之上实现 [RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000) 并使用 [Unreliable Datagram Extension](https://datatracker.ietf.org/doc/rfc9221/).

所有多字节（"multibyte"） 数字使用大端格式.

所有可变长度整数（"varints"）按照 QUIC (RFC 9000) 中定义的方式编码/解码

## 认证与 HTTP/3 伪装

Hysteria 协议的一个关键特性是，对于没有适当认证凭证的第三方（无论是中间人还是主动探测），Hysteria 代理服务器对其表现为一个标准的 HTTP/3 网络服务器，攻击者无法区分代理加密流量与正常的 HTTP/3 流量。

因此，Hysteria 服务器必须实现一个 HTTP/3 服务器（如 [RFC 9114](https://datatracker.ietf.org/doc/rfc9114/)）并像任何标准的网络服务器一样处理 HTTP 请求。为了防止主动探测器检测到 Hysteria 服务器中的响应模式，实现应当建议用户托管实际内容，或将其设置为其他站点的反向代理。

一个 Hysteria 客户端在连接时必须向服务器发送以下 HTTP/3 请求：

```
:method: POST
:path: /auth
:host: hysteria
Hysteria-Auth: [string]
Hysteria-CC-RX: [uint]
Hysteria-Padding: [string]
```

`Hysteria-Auth`: 认证凭证

`Hysteria-CC-RX`: 客户端的最大接收速率，单位为每秒字节数。数值为 0 表示未知

`Hysteria-Padding`: 可变长度的随机填充字符串

Hysteria 服务器必须识别这个特殊请求，而不是提供（用于伪装的）内容或站点转发。服务器必须使用提供的信息对客户端进行认证。如果认证成功，服务器必须发送以下响应（HTTP 状态码 233）：

```
:status: 233 HyOK
Hysteria-UDP: [true/false]
Hysteria-CC-RX: [uint/"auto"]
Hysteria-Padding: [string]
```

`Hysteria-UDP`: 服务器是否支持 UDP 中继

`Hysteria-CC-RX`: 服务器的最大接收速率，单位为每秒字节数。数值为 0 表示无限制；“自动”表示服务器拒绝提供数值，并要求客户端使用拥塞控制自行确定速率

`Hysteria-Padding`: 可变长度的随机填充字符串

关于如何使用 `Hysteria-CC-RX`， 请参阅”拥塞控制“部分.

`Hysteria-Padding` 是可选的，仅用于混淆请求/响应模式。双方都应忽略它。

如果认证失败，服务器必须表现得像一个不理解该请求的标准网络服务器，如果配置了反向代理，将请求转发到上游站点并将响应返回给客户端。

客户端必须检查状态码以确定认证是否成功。如果状态码不是 233，客户端必须认为认证失败并断开与服务器的连接。

在且仅在客户端通过认证之后，服务器必须将这个 QUIC 连接视为 Hysteria 代理连接。然后它必须开始处理来自客户端的代理请求，如下一节所述。

## 代理协议格式

### TCP

对于每个 TCP 连接，客户端必须创建一个新的 QUIC 双向流，并发送以下 TCPRequest 消息：

```
[varint] 0x401 (TCPRequest ID)
[varint] Address length
[bytes] Address string (host:port)
[varint] Padding length
[bytes] Random padding
```

服务器必须回复一个 TCPResponse 消息:

```
[uint8] Status (0x00 = OK, 0x01 = Error)
[varint] Message length
[bytes] Message string
[varint] Padding length
[bytes] Random padding
```


如果状态为 OK，服务器必须开始在客户端和指定的 TCP 地址之间转发数据，直到任一方关闭连接。如果状态为错误，服务器必须关闭 QUIC 流。

### UDP

UDP 数据包必须被封装在以下 UDPMessage 格式中，并通过 QUIC 的不可靠数据报发送（同时适用于客户端到服务器和服务器到客户端）：

```
[uint32] Session ID
[uint16] Packet ID
[uint8] Fragment ID
[uint8] Fragment count
[varint] Address length
[bytes] Address string (host:port)
[bytes] Payload
```

客户端必须为每个 UDP 会话使用唯一的Session ID。除非服务器有其他机制来区分不同会话的数据包（例如，对称 NAT，不同的出站 IP 地址等），否则应为每个会话 ID 分配一个唯一的 UDP 端口。

协议没有提供明确的方式来关闭 UDP 会话。虽然客户端可以无限期地保留和重用会话 ID，但服务器应在一段不活动时间后（或根据其他标准）释放并重新分配与会话 ID 关联的端口。如果客户端向服务器不再识别的会话 ID 发送 UDP 数据包，服务器必须将其视为新会话并分配新端口。

如果服务器不支持 UDP 中继，应静默丢弃从客户端收到的所有 UDP 消息。

#### 分片

由于 QUIC 不可靠数据报通道的限制，任何超过 QUIC 最大数据报大小的 UDP 数据包必须被分片或丢弃。

对于被分片的数据包，每个分片必须携带相同的唯一数据包 ID。分片 ID 从 0 开始，表示总分片数的索引。服务器和客户端必须等待一个被分片的数据包的所有分片到达后才能处理它们。如果一个数据包的一个或多个分片丢失，整个数据包必须被丢弃。

对于未被分片的数据包，分片数必须设置为 1。在这种情况下，无需考虑数据包 ID 和分片 ID 的值。

## 拥塞控制

Hysteria 的一个独特功能是能够在客户端设置 tx/rx（上传/下载）速率。在认证过程中，客户端通过 `Hysteria-CC-RX` 头将其接收速率发送给服务器。服务器可以使用这个信息来确定对客户端的传输速率，反之亦然，通过相同的头将其接收速率返回给客户端。

三个特殊情况如下：

- 如果客户端发送 0，表示它不知道自己的接收速率。服务器必须使用拥塞控制算法（例如，BBR、Cubic）来调整其传输速率。
- 如果服务器回应 0，表示它没有带宽限制。客户端可以以任何速率传输。
- 如果服务器回应“自动”，表示它选择不指定速率。客户端必须使用拥塞控制算法来调整其传输速率。

## "Salamander" 混淆

Hysteria 协议支持一个可选的混淆层： "Salamander"。该层使用以下方法封装所有QUIC数据包

```
[8 bytes] Salt
[bytes] Payload
```

对于每个 QUIC 数据包，混淆算法必须计算一个随机生成的 8 字节盐加上用户预设的共享密钥所得到的 BLAKE2b-256 哈希值。

```
hash = BLAKE2b-256(key + salt)
```

然后使用以下算法混淆数据：

```
for i in range(0, len(payload)):
    payload[i] ^= hash[i % 32]
```

解码器必须使用相同的算法来计算加盐哈希并计算出载荷。任何无效的数据包必须被丢弃。
