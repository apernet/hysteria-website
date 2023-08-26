# Installation

Like any proxy software, Hysteria consists of a server and a client. Our precompiled executables for all platforms include both modes. This means you can use it as either a server or a client on any platform we support. Below are your download options:

- [GitHub Releases](https://github.com/apernet/hysteria/releases) ([What build should I choose?](#what-build-should-i-choose))

TODO: more options

## What build should I choose?

Files are named using the format `hysteria-[platform]-[arch]` (`darwin` refers to macOS).

For most Windows/Linux PCs and servers, the most common architecture is `amd64`, also known as `x86-64`. A special build for `amd64` processors with AVX support is available as `amd64-avx`. Most modern `amd64` processors should support AVX, so we recommend trying this version first, and switching to the non-AVX version only if you run into problems.

For Macs with the M1 chip or newer, use the `arm64` version. Older Macs should use the `amd64` version.

TODO: table
