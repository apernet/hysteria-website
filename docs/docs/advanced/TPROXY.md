# Setting up TPROXY

Since version 2.2, the Linux kernel has included support for TProxy, which allows transparent proxying of both TCP and UDP traffic. This feature is particularly useful if you are running a Linux-based router and want to proxy traffic passing through it. For more detailed and accurate information, please refer to [the official documentation on TProxy](https://docs.kernel.org/networking/tproxy.html).

## TCP example

Assume you have the following Hysteria client configuration:

```yaml
tcpTProxy:
  listen: 127.0.0.1:2500
```

First, we create a new chain called `DIVERT` in the `mangle` table, add a rule to the `PREROUTING` chain to make TCP packets jump to the `DIVERT` chain, and in the `DIVERT` chain we mark the packets with `1`. The reason we mark the packets is so we can use a separate routing table for them later.

```bash
iptables -t mangle -N DIVERT
iptables -t mangle -A PREROUTING -p tcp -m socket -j DIVERT
iptables -t mangle -A DIVERT -j MARK --set-mark 1
iptables -t mangle -A DIVERT -j ACCEPT
```

Next, we add a new routing rule to use table 100 for packets marked with `1`, and add a route to this table 100 to deliver those packets locally.

```bash
ip rule add fwmark 1 lookup 100
ip route add local 0.0.0.0/0 dev lo table 100
```

Finally, we add another rule to the `PREROUTING` chain to match incoming TCP traffic with destination port 443 and redirect it to our proxy. **This example redirects only TCP port 443, but you can remove the `--dport 443` part to redirect all TCP traffic, or change it as needed.**

```bash
iptables -t mangle -A PREROUTING -p tcp --dport 443 -j TPROXY --tproxy-mark 0x1/0x1 --on-ip 127.0.0.1 --on-port 2500
```

## UDP example

Assume you have the following Hysteria client configuration:

```yaml
udpTProxy:
  listen: 127.0.0.1:2500
```

The steps to set up the `DIVERT` chain and routing table are the same as the TCP example above. The only difference is that we need a UDP rule in the `PREOUTING` chain instead:

```bash
iptables -t mangle -A PREROUTING -p udp -m socket -j DIVERT
```

And we add a rule to the `PREROUTING` chain to match incoming UDP traffic with destination port 53 and redirect it to our proxy.

```bash
iptables -t mangle -A PREROUTING -p udp --dport 53 -j TPROXY --tproxy-mark 0x1/0x1 --on-ip 127.0.0.1 --on-port 2500
```
