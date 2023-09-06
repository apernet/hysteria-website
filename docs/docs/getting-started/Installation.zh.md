# 安装

像其他代理软件一样，Hysteria 由服务端和客户端组成。我们的可执行文件在所有平台上都包括这两种模式。**可以通过以下几种方式之一获取最新版本：**

- [GitHub Releases](https://github.com/apernet/hysteria/releases) ([我该选择哪个版本？](#_2))
- [Linux 服务端部署脚本](#linux)
- [Arch Linux AUR](https://aur.archlinux.org/packages/hysteria)
- 使用 [第三方应用](3rd-party-apps.md)
- [自行从源码编译](../developers/Build.md)

## 我该选择哪个版本？

文件名采用 `hysteria-[平台]-[架构]` 的格式（`darwin` 指的是 macOS）。

对于 Windows/Linux 的电脑和服务器，最常见的架构是 `amd64`，也称 `x86-64`。有一个为带 AVX 支持的 `amd64` 处理器提供的版本，即 `amd64-avx`。大多数现代处理器应该都支持 AVX，因此我们建议首先尝试这个版本，遇到问题再切换到非 AVX 版本。

对于是 M1 芯片或更新版本的 Mac，使用 `arm64` 版本。老的 Mac 应使用 `amd64` 版本。

| 文件名                         | 系统    | 架构   | 备注                   |
| ------------------------------ | ------- | ------ | ---------------------- |
| hysteria-windows-amd64.exe     | Windows | x86-64 |                        |
| hysteria-windows-amd64-avx.exe | Windows | x86-64 | 需要 AVX               |
| hysteria-windows-386.exe       | Windows | x86    |                        |
| hysteria-windows-arm64.exe     | Windows | ARM64  |                        |
| hysteria-darwin-amd64          | macOS   | x86-64 |                        |
| hysteria-darwin-amd64-avx      | macOS   | x86-64 | 需要 AVX               |
| hysteria-darwin-arm64          | macOS   | ARM64  | M1 以上                |
| hysteria-linux-amd64           | Linux   | x86-64 |                        |
| hysteria-linux-amd64-avx       | Linux   | x86-64 | 需要 AVX               |
| hysteria-linux-386             | Linux   | x86    |                        |
| hysteria-linux-arm             | Linux   | ARMv7  |                        |
| hysteria-linux-armv5           | Linux   | ARMv5  |                        |
| hysteria-linux-arm64           | Linux   | ARM64  |                        |
| hysteria-linux-s390x           | Linux   | s390x  |                        |
| hysteria-linux-mipsle          | Linux   | MIPS   | 小端序                 |
| hysteria-linux-mipsle-sf       | Linux   | MIPS   | 小端序, 无硬件浮点支持 |
| hysteria-freebsd-amd64         | FreeBSD | x86-64 |                        |
| hysteria-freebsd-amd64-avx     | FreeBSD | x86-64 | 需要 AVX               |
| hysteria-freebsd-386           | FreeBSD | x86    |                        |
| hysteria-freebsd-arm           | FreeBSD | ARMv7  |                        |
| hysteria-freebsd-arm64         | FreeBSD | ARM64  |                        |

## Linux 服务端部署脚本

我们提供了一个 bash 脚本，可以在常见的 Linux 发行版上自动下载最新版本的 Hysteria 并配置 systemd 服务。

```bash
sudo bash <(curl -fsSL https://get.hy2.sh/)
```
