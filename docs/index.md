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

<h2 style="text-align: center;">Hysteria is a powerful, lightning fast and censorship resistant proxy.</h2>

<p align="center">
  <a href="docs/getting-started/Installation/" style="padding: 14px 28px; background-color: #4A7B9D; color: white; border: none; border-radius: 8px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.25);">
    Get Started (English)
  </a>
  <a href="zh/" style="padding: 14px 28px; background-color: #D67676; color: white; border: none; border-radius: 8px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; box-shadow: 0px 4px 8px 0px rgba(0,0,0,0.25);">
    中文文档 (Chinese)
  </a>
</p>

<h4 style="text-align: center;">Open-source MIT licensed. <a href="https://github.com/apernet/hysteria">Code on GitHub</a></h4>

---

<div class="feature-grid">
  <div>
    <h3>🛠️ Packed to the gills</h3>
    <p>Expansive range of modes including SOCKS5, HTTP proxy, TCP/UDP forwarding, Linux TProxy - not to mention additional features continually being added.</p>
  </div>

  <div>
    <h3>⚡ Lightning fast</h3>
    <p>Powered by a custom QUIC protocol, Hysteria delivers unparalleled performance over even the most unreliable and lossy networks.</p>
  </div>

  <div>
    <h3>✊ Censorship resistant</h3>
    <p>Our protocol is designed to masquerade as standard HTTP/3 traffic, making it very difficult to detect and block without widespread collateral damage.</p>
  </div>
  
  <div>
    <h3>💻 Cross-platform</h3>
    <p>We have builds for all major platforms and architectures. Deploy anywhere & use everywhere.</p>
  </div>

  <div>
    <h3>🔗 Easy integration</h3>
    <p>With built-in support for custom authentication, traffic statistics & access control, Hysteria is easy to integrate into your infrastructure.</p>
  </div>
  
  <div>
    <h3>🤗 Open standards</h3>
    <p>We have well-documented specifications and code for developers to contribute and build their own apps.</p>
  </div>
</div>
