# 我不喜欢 YAML 怎么办？

尽管文档使用的都是 YAML，Hysteria 实际上也完全支持使用 JSON 作为配置文件。

## JSON 示例

```json
{
  "server": "your.server.net",
  "auth": "i_still_love_jason",
  "bandwidth": {
    "up": "30 mbps",
    "down": "100 mbps"
  },
  "fastOpen": true,
  "lazy": true,
  "socks5": {
    "listen": "127.0.0.1:1080"
  },
  "http": {
    "listen": "127.0.0.1:8080"
  }
}
```

将文件命名为 `config.json`，然后用以下命令运行客户端：

```bash
./hysteria-linux-amd64-avx -c config.json
```

## 转换

如果你已经有了一个 YAML 配置文件，可以使用 `yq` (https://github.com/mikefarah/yq) 将其转换为 JSON：

```bash
yq config.yaml -o json > config.json
```
