# 日志

Hysteria 提供以下日志级别，可以通过 `HYSTERIA_LOG_LEVEL` 环境变量进行控制：

- `debug`
- `info`（默认）
- `warn`
- `error`

还可以使用 `HYSTERIA_LOG_FORMAT` 环境变量来控制日志格式：

- `console`（默认）
- `json`（时间将以 Unix epoch 毫秒形式显示）

Hysteria 默认会检查版本更新，并在有新版本时打印日志消息。要禁用此功能，将 `HYSTERIA_DISABLE_UPDATE_CHECK` 设置为 1。
