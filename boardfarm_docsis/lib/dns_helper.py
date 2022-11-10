from nested_lookup import nested_lookup


def dns_acs_config(devices, dns_dict):
    if dns_dict:
        for dev, host_data in dns_dict.items():
            d = getattr(devices, dev.lower())
            ipv4 = nested_lookup("ipv4", host_data)
            ipv6 = nested_lookup("ipv6", host_data)
            d.dns.configure_hosts(
                reachable_ipv4=ipv4[0].get("reachable", 0) if ipv4 else 0,
                unreachable_ipv4=ipv4[0].get("unreachable", 0) if ipv4 else 0,
                reachable_ipv6=ipv6[0].get("reachable", 0) if ipv6 else 0,
                unreachable_ipv6=ipv6[0].get("unreachable", 0) if ipv6 else 0,
            )
