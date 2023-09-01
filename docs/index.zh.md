---
title: Home
hide:
  - navigation
  - toc
---

<!-- Hack to hide the title -->
<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

<!-- Make the feature grid responsive -->
<style>
  .feature-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }
  @media (min-width: 600px) {
    .feature-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
  @media (min-width: 900px) {
    .feature-grid {
      grid-template-columns: 1fr 1fr 1fr;
    }
  }
</style>

![Hysteria 2 Logo Banner](./assets/banner_light.svg#logo-light){: style="width: 80%; margin: 0 auto;"}
![Hysteria 2 Logo Banner](./assets/banner_dark.svg#logo-dark){: style="width: 80%; margin: 0 auto;"}

<h2 style="text-align: center;">Hysteria 是一个强大、快速、抗审查的代理工具。</h2>

<p align="center">
  <a href="docs/getting-started/Installation/" style="padding: 14px 28px; background-color: #4A7B9D; color: white; border: none; border-radius: 8px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.25);">
    了解一下
  </a>
</p>

<h4 style="text-align: center;">开源 MIT 许可。 <a href="https://github.com/apernet/hysteria">GitHub 代码</a></h4>

---

<div class="feature-grid">
  <div>
    <h3>🛠️ 功能齐全</h3>
    <p>SOCKS5、HTTP 代理、TCP/UDP 转发、Linux TProxy，更多模式不断添加中。</p>
  </div>

  <div>
    <h3>⚡ 快如闪电</h3>
    <p>通过魔改的 QUIC 协议驱动，Hysteria 即使在最不稳定和容易丢包的网络环境中也能提供无与伦比的性能。</p>
  </div>

  <div>
    <h3>✊ 抗封锁能力</h3>
    <p>协议旨在伪装成标准的 HTTP/3 流量，无论中间人还是主动探测，都很难分辨和封锁。</p>
  </div>
  
  <div>
    <h3>💻 跨平台</h3>
    <p>我们为所有主要的平台和架构提供构建。随处部署，随处使用。</p>
  </div>

  <div>
    <h3>🔗 易于集成</h3>
    <p>内置对自定义认证、流量统计和访问控制的支持，Hysteria 很容易集成到已有的后端中。</p>
  </div>
  
  <div>
    <h3>🤗 开放标准</h3>
    <p>我们有详尽的文档、规范和代码，供开发者参考、贡献和构建自己的应用。</p>
  </div>

</div>
