# Installation

Like any proxy software, Hysteria consists of a server and a client. Our precompiled executables includes both modes on all platforms. **You can download our latest releases using one of the following options:**

- [GitHub Releases](https://github.com/apernet/hysteria/releases) ([What build should I choose?](#what-build-should-i-choose))
- [Deployment script for Linux servers](#deployment-script-for-linux-servers)
- [Arch Linux AUR](https://aur.archlinux.org/packages/hysteria)
- [Docker images](#docker-images)
- Use [3rd-party apps](3rd-party-apps.md)
- [Build from source](../developers/Build.md)

## What build should I choose?

Files are named using the format `hysteria-[platform]-[arch]` (`darwin` refers to macOS).

For Windows/Linux PCs and servers, the most common architecture is `amd64`, also known as `x86-64`. A special build for `amd64` processors with AVX support is available as `amd64-avx`. Most modern processors should support AVX, so we recommend trying this version first, and switching to the non-AVX version only if you run into problems.

For Macs with the M1 chip or newer, use the `arm64` version. Older Macs should use the `amd64` version.

| File                           | OS      | Arch   | Note                      |
| ------------------------------ | ------- | ------ | ------------------------- |
| hysteria-windows-amd64.exe     | Windows | x86-64 |                           |
| hysteria-windows-amd64-avx.exe | Windows | x86-64 | Requires AVX              |
| hysteria-windows-386.exe       | Windows | x86    |                           |
| hysteria-windows-arm64.exe     | Windows | ARM64  |                           |
| hysteria-darwin-amd64          | macOS   | x86-64 |                           |
| hysteria-darwin-amd64-avx      | macOS   | x86-64 | Requires AVX              |
| hysteria-darwin-arm64          | macOS   | ARM64  | M1 or newer               |
| hysteria-linux-amd64           | Linux   | x86-64 |                           |
| hysteria-linux-amd64-avx       | Linux   | x86-64 | Requires AVX              |
| hysteria-linux-386             | Linux   | x86    |                           |
| hysteria-linux-arm             | Linux   | ARMv7  |                           |
| hysteria-linux-armv5           | Linux   | ARMv5  |                           |
| hysteria-linux-arm64           | Linux   | ARM64  |                           |
| hysteria-linux-s390x           | Linux   | s390x  |                           |
| hysteria-linux-mipsle          | Linux   | MIPS   | Little Endian             |
| hysteria-linux-mipsle-sf       | Linux   | MIPS   | Little Endian, Soft Float |
| hysteria-android-amd64         | Android | x86-64 |                           |
| hysteria-android-386           | Android | x86    |                           |
| hysteria-android-armv7         | Android | ARMv7  |                           |
| hysteria-android-arm64         | Android | ARM64  |                           |
| hysteria-freebsd-amd64         | FreeBSD | x86-64 |                           |
| hysteria-freebsd-amd64-avx     | FreeBSD | x86-64 | Requires AVX              |
| hysteria-freebsd-386           | FreeBSD | x86    |                           |
| hysteria-freebsd-arm           | FreeBSD | ARMv7  |                           |
| hysteria-freebsd-arm64         | FreeBSD | ARM64  |                           |

## Deployment script for Linux servers

We provide a bash script that automatically downloads the latest version of Hysteria and configures a systemd service on common Linux distributions.

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

## Docker images

Our official Docker images are hosted on Docker Hub: https://hub.docker.com/r/tobyxdd/hysteria

### Compose example

```yaml
version: "3.9"
services:
  hysteria:
    image: tobyxdd/hysteria
    container_name: hysteria
    restart: always
    network_mode: "host"
    volumes:
      - acme:/acme
      - ./hysteria.yaml:/etc/hysteria.yaml
    command: ["server", "-c", "/etc/hysteria.yaml"]
volumes:
  acme:
```
