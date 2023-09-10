# What if I hate YAML?

Even though our documentation uses YAML, Hysteria actually has full support for JSON configuration files.

## JSON example

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

Name the file `config.json` and run the client with the following command:

```bash
./hysteria-linux-amd64-avx -c config.json
```

## Conversion

If you already have a YAML configuration file, you can convert it to JSON using `yq` (https://github.com/mikefarah/yq):

```bash
yq config.yaml -o json > config.json
```
