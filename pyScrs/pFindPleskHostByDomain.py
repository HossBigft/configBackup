import argparse
from dns import resolver, reversename
import sys
import nsZoneMaster
import pFindSubscriptionByDomain as pfind
import re
from termcolor import colored


DNS_HOSTING_HOSTNAME = "dns.hoster.kz."


class AmbiguousMXRecordTargets(Exception):
    def __init__(self, mx_record, message=None):
        self.mx_record = mx_record
        self.message = (
            message or f"Multiple A records found for MX record [{mx_record}]."
        )
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PTRValidationError(Exception):
    def __init__(self, ptr_record, message=None):
        self.ptr_record = ptr_record
        self.message = (
            message
            or f'PTR record does not contain subsctring "hoster.kz" [{ptr_record}].'
        )
        super().__init__(self.message)

    def __str__(self):
        return self.message


class RecordNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


def regex_type(pattern: str | re.Pattern):
    """Argument type for matching a regex pattern."""

    def closure_check_regex(arg_value):
        if not re.match(pattern, arg_value):
            raise argparse.ArgumentTypeError(
                f"Invalid domain name: '{arg_value}' is not a valid domain name"
            )
        return arg_value

    return closure_check_regex


def resolve_a_record(domain):
    try:
        return "".join([ipval.to_text() for ipval in resolver.resolve(domain, "A")])
    except (resolver.NoAnswer, resolver.NXDOMAIN, resolver.NoNameservers) as exc:
        raise RecordNotFoundError(f"A record not found for {domain}") from exc


def resolve_ptr_record(ip):
    try:
        addr_record = reversename.from_address(ip)
        return str(resolver.resolve(addr_record, "PTR")[0])
    except (resolver.NoAnswer, resolver.NXDOMAIN) as exc:
        raise RecordNotFoundError(f"PTR record not found for {ip}") from exc


def main():
    parser = argparse.ArgumentParser(
        description="Tries to find Plesk server hostname by given domain"
    )

    parser.add_argument(
        "domain",
        type=regex_type(r"(?:(?!-|[^.]+_)[A-Za-z0-9-_]{1,63}(?<!-)(?:\.|$)){2,}"),
        help="domain name of the site to search",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enables detailed output in the console",
    )
    args = parser.parse_args()
    domain = args.domain
    verbose_flag = args.verbose
    if verbose_flag:
        print(f"Starting host resolution for {domain} using A record.")

    try:
        a_record = resolve_a_record(domain)
        try:
            ptr_record = resolve_ptr_record(a_record)
            if "hoster.kz" in ptr_record and not ptr_record == DNS_HOSTING_HOSTNAME:
                print(ptr_record)
                sys.exit(0)
            else:
                raise PTRValidationError(ptr_record)
        except RecordNotFoundError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] PTR record not found for {a_record} PTR lookup failed."
                )
        except PTRValidationError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] No substring 'hoster.kz' in {ptr_record}"
                )
    except RecordNotFoundError:
        if verbose_flag:
            print(f"[{colored('FAIL','yellow')}] A record not found for {domain}")

    if verbose_flag:
        print(f"Attempting to resolve host for {domain} using MX record.")
    try:
        mx_record = "".join(
            [ipval.to_text() for ipval in resolver.resolve(domain, "MX")]
        ).split(" ")[1]

        a_record: str
        if len(a_records := resolve_a_record(mx_record)) > 1:
            raise AmbiguousMXRecordTargets(mx_record)
        else:
            a_record = a_records[0]

        try:
            ptr_record = resolve_ptr_record(a_record)
            if "hoster.kz" in ptr_record and not ptr_record == DNS_HOSTING_HOSTNAME:
                print(ptr_record)
                sys.exit(0)
            else:
                raise PTRValidationError(ptr_record)

        except RecordNotFoundError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] PTR record not found for {mx_record}"
                )
        except PTRValidationError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] No substring 'hoster.kz' in {ptr_record}"
                )
    except RecordNotFoundError:
        if verbose_flag:
            print(f"[{colored('FAIL','yellow')}] MX record not found for {domain}")
    except AmbiguousMXRecordTargets:
        if verbose_flag:
            print(
                f"[{colored('FAIL','yellow')}] Multiple A records for MX record {mx_record} Ambioguous mail host."
            )

    if verbose_flag:
        print(f"Attempting to resolve host for {domain} using DNS zone master.")

    if zone_master_a_record := "".join(
        nsZoneMaster.getDomainZoneMaster(domain, verbosity_flag=False)["zone_master"]
    ):
        try:
            ptr_record = resolve_ptr_record(zone_master_a_record)
            if "hoster.kz" in ptr_record and not ptr_record == DNS_HOSTING_HOSTNAME:
                print(ptr_record)
                sys.exit(0)
            else:
                raise PTRValidationError(ptr_record)
        except RecordNotFoundError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] PTR record not found for {a_record} PTR lookup failed."
                )
        except PTRValidationError:
            if verbose_flag:
                print(
                    f"[{colored('FAIL','yellow')}] No substring 'hoster.kz' in {ptr_record}"
                )
    else:
        if verbose_flag:
            print(f"[{colored('FAIL','yellow')}] Zone master not found for {domain}.")

    if verbose_flag:
        print(f"Attempting to find host {domain} by querying servers.")
    if answers := [
        answer
        for answer in pfind.query_domain_info(domain, verbose_flag=False)
        if not answer["host"] == DNS_HOSTING_HOSTNAME
    ]:
        if (hosts_num := len(answers)) > 1:
            print(
                f"[{colored('ERROR','red')}] Multiple hosts found [{hosts_num}] The actual host is ambiguous."
            )
            for answer in answers:
                print(answer["host"])
            sys.exit(1)
        else:
            for answer in answers:
                print(answer["host"])
            sys.exit(0)
    else:
        if verbose_flag:
            print(f"[{colored('ERROR','red')}] Host for {domain} not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
