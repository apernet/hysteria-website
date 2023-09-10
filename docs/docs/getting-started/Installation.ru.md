# Установка

Как и любое программное обеспечение для прокси, Hysteria состоит из серверной и клиентской части. Наши предварительно скомпилированные исполняемые файлы включают в себя оба режима для всех платформ. **Вы можете скачать наши последние версии, используя одну из следующих опций:**

- [Релизы на GitHub](https://github.com/apernet/hysteria/releases) ([Какой сборку выбрать?](#какой-сборку-выбрать))
- [Скрипт развертывания для серверов Linux](#скрипт-развертывания-для-серверов-linux)
- [Arch Linux AUR](https://aur.archlinux.org/packages/hysteria)
- [Образы Docker](#образы-docker)
- Использовать [приложения от третьих сторон](3rd-party-apps.md)
- [Сборка из исходного кода](../developers/Build.md)

## Какой сборку выбрать?

Файлы имеют имя в формате `hysteria-[платформа]-[архитектура]` (`darwin` означает macOS).

Для ПК и серверов на Windows/Linux наиболее распространенной архитектурой является `amd64`, также известная как `x86-64`. Специальная сборка для процессоров `amd64` с поддержкой AVX доступна как `amd64-avx`. Большинство современных процессоров должны поддерживать AVX, поэтому мы рекомендуем сначала попробовать эту версию, и переключиться на версию без AVX только в случае возникновения проблем.

Для Mac с чипом M1 или новее используйте версию `arm64`. Старые модели Mac должны использовать версию `amd64`.

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
| hysteria-freebsd-amd64         | FreeBSD | x86-64 |                           |
| hysteria-freebsd-amd64-avx     | FreeBSD | x86-64 | Requires AVX              |
| hysteria-freebsd-386           | FreeBSD | x86    |                           |
| hysteria-freebsd-arm           | FreeBSD | ARMv7  |                           |
| hysteria-freebsd-arm64         | FreeBSD | ARM64  |                           |

## Скрипт развертывания для серверов Linux

Мы предоставляем bash-скрипт, который автоматически скачивает последнюю версию Hysteria и настраивает службу systemd на распространенных дистрибутивах Linux.

```bash
bash <(curl -fsSL https://get.hy2.sh/)
```

## Образы Docker

[Наши официальные образы Docker размещены на Docker Hub.](https://hub.docker.com/r/tobyxdd/hysteria)

### Пример с использованием Compose

```yaml
version: "3.9"
services:
  hysteria:
    image: tobyxdd/hysteria
    container_name: hysteria
    restart: always
    network_mode: "host"
    volumes:
      - ./hysteria.yaml:/etc/hysteria.yaml
    command: ["server", "-c", "/etc/hysteria.yaml"]
```
