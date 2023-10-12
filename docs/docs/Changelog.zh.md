---
title: 更新日志
hide:
  - navigation
---

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
