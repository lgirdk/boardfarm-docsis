def dns_acs_config(devices, dns_dict):
    if dns_dict:
        for dev, host_data in dns_dict.items():
            d = getattr(devices, dev.lower())
            d.dns.configure_hosts(
                reachable_ips=host_data["num_reachable_ip"],
                unreachable_ips=host_data["num_unreachable_ip"],
            )
