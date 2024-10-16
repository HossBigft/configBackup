from host_lists import DNS_SERVER_LIST
import async_ssh_executor as ase


def getDomainZoneMaster(
    domain_name, verbosity_flag=True, test_flag=False, debug_flag=False
):
    getZoneMasterCmd = f"cat /var/opt/isc/scls/isc-bind/zones/_default.nzf| grep '\\\"{''.join(domain_name)}\\\"' | grep -Po '((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\\b){{4}}' | head -n1"
    dnsAnswers = []
    dnsAnswers = ase.batch_ssh_command_result(
        server_list=DNS_SERVER_LIST,
        command=getZoneMasterCmd,
        verbose=debug_flag,
    )
    if verbosity_flag:
        return {"domain": f"{domain_name}", "answers": dnsAnswers}

    unique_zone_masters = list(set(answer["stdout"] for answer in dnsAnswers))
    return {
        "domain": domain_name,
        "zone_master": unique_zone_masters,
    }
