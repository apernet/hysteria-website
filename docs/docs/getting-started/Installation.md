# Installation

Like any proxy software, Hysteria consists of a server and a client. Our precompiled executables includes both modes on all platforms. You can download our latest releases using one of the following options:

- [GitHub Releases](https://github.com/apernet/hysteria/releases) ([What build should I choose?](#what-build-should-i-choose))

TODO: more options

## What build should I choose?

Files are named using the format `hysteria-[platform]-[arch]` (`darwin` refers to macOS).

For Windows/Linux PCs and servers, the most common architecture is `amd64`, also known as `x86-64`. A special build for `amd64` processors with AVX support is available as `amd64-avx`. Most modern processors should support AVX, so we recommend trying this version first, and switching to the non-AVX version only if you run into problems.

For Macs with the M1 chip or newer, use the `arm64` version. Older Macs should use the `amd64` version.

TODO: table
