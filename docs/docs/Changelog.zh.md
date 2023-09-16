---
title: 更新日志
hide:
  - navigation
---

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
