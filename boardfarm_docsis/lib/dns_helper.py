def dns_acs_config(devices, dns_dict):
    if dns_dict:
        for dev, host_data in dns_dict.items():
            d = getattr(devices, dev.lower())
            d.dns.configure_hosts(
                reachable_ipv4=host_data["ipv4"]["reachable"],
                unreachable_ipv4=host_data["ipv4"]["unreachable"],
                reachable_ipv6=host_data["ipv6"]["reachable"],
                unreachable_ipv6=host_data["ipv6"]["unreachable"],
            )
