---
title: 更新日志
hide:
  - navigation
---

## 2.2.3

- 修复了即使显式使用 IPv4/IPv6 监听地址（如 `0.0.0.0:443` 或 `[::]:443`）仍会同时监听 IPv4/IPv6 的问题
- 开启懒狗模式的情况下，服务器域名解析推迟到需要连接时
- 每次 TLS 握手时都会重新读取本地证书，以便用户能够在不重启服务器的情况下更新文件

## 2.2.2

- 修复了上个版本引入的一个导致客户端无法自动重连的 bug
- ACL 新增 `suffix:` 支持，用来匹配一个域名和其所有子域名 (例如 `reject(suffix:baidu.com)`)

## 2.2.1

- 添加了 GeoIP 和 GeoSite 自动更新功能（ACL 下的 `geoUpdateInterval` 字段，默认为一周）
- 客户端现在在连接到服务器后会显示握手信息，目前包括 UDP 转发是否开启和协商的传输速率
- 带宽单位换算（Kbps/Mbps/Gbps/Tbps）从 1024 改为 1000
- 添加了 RISC-V (riscv64) 支持
- quic-go 更新到 v0.40.0

## 2.2.0

- ACL 新增 GeoSite 支持 (GeoIP 和 GeoSite 现在都使用 v2ray 的 "dat" 格式数据库)
- ACL 新增对非英文域名 (IDN) 的支持 (例如 `v6_only(战狼*.中国)`)
- 伪装 (masquerade) proxy 模式添加 WebSocket 支持
- 流量统计 API 新增基于密钥 (secret) 的认证
- 修复某些 Linux 系统上的兼容性问题

## 2.1.1

> 此版本包含重要修复，强烈建议更新

- 修复一个通过构造特殊的 UDP message 包可以导致服务端崩溃的问题
- 修复 FreeBSD 上的兼容性问题
- Windows 用户现在可以通过双击 exe 文件直接启动程序了

## 2.1.0

- 修复 BBR 内存泄漏问题
- 微调 Brutal 拥塞控制
- 伪装 (masquerade) 新增字符串 (string) 模式
- 出站 (outbound) 新增 HTTP/HTTPS 代理

## 2.0.4

- 优化并修复 Brutal 拥塞控制中的一些问题
- 修复 BBR 在特定条件下导致连接卡死且 CPU 占用飙升的问题
- 修复两个线程安全问题
- 新增 `HYSTERIA_BRUTAL_DEBUG` 环境变量，开启后可输出当前延迟、丢包率、MTU 等信息

## 2.0.3

> 此版本包含重要修复，强烈建议更新

- **[重要]** 修复在使用 BBR (即客户端不写带宽，或服务端开启了 `ignoreClientBandwidth`) 的情况下，由于 BBR 实现的 bug 导致无法准确判断带宽上限，发包速率过快的问题。
- 修复 ZeroSSL 缺少 EAB 无法获取证书的问题

## 2.0.2

- 修复在某些设备上由于不支持 GSO 导致的无法连接/断流问题
- 新增 HTTP/HTTPS (TCP) 伪装服务器
- 新增 Android 构建

## 2.0.1

- 新增 TCP Redirect 模式
- 在日志中输出伪装模式收到的 HTTP 请求 (debug 级别)
- 新增环境变量 `HYSTERIA_ACME_DIR`，用于设置 ACME 目录的位置

## 2.0.0

这是 Hysteria 2 的第一个稳定版本。几乎完全重写了 Hysteria 原有的代码，包括新的协议、新的功能和各种改进。
