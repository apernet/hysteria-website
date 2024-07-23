# 流量统计 API

如果配置中设置了 API secret，调用时需要在请求头加上 `Authorization` 标头。

请求：

```shell
curl -H 'Authorization: secret' http://ip:port/path
```

### GET `/traffic`

此接口返回一个 JSON map，是每个用户的流量信息。

响应：

```json
{
  "wang": {
    "tx": 514,
    "rx": 4017
  },
  "joe": {
    "tx": 7790,
    "rx": 446623
  }
}
```

还可以使用参数 `clear` 在返回统计数据后将其清零：

```
/traffic?clear=1
```

### POST `/kick`

此接口可以提交一个要踢下线的用户列表。

请求：

```json
["wang", "joe"]
```

> **注意：** 由于客户端内置了重连逻辑，被踢出后将尝试重新连接。为了避免需要反复踢出同一个用户，应该同时在验证后端中屏蔽该用户。

### GET `/online`

此接口返回一个 JSON map，是当前在线的用户与其对应的连接数。这里的连接数指的是 Hysteria 客户端实例的数量（可以理解为设备数），而非代理连接数。

响应：

```json
{
  "wang": 2,
  "joe": 1
}
```
