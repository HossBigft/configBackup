import re

from host_lists import PLESK_SERVER_LIST
from enum import IntEnum
from typing import List, TypedDict

import ssh_async_executor as ase


class QueryResult(TypedDict):
    host: str
    id: str
    name: str
    username: str
    userlogin: str
    domains: List[str]
    domain_states: List[str]
    is_space_overused: bool
    subscription_size_mb: int
    subscription_status: str


DOMAIN_REGEX_PATTERN_STRICT = (
    r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,8}$"
)

DOMAIN_REGEX_PATTERN_PARTIAL = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))$"


class DomainStatus(IntEnum):
    ONLINE = 0
    SUBSCRIPTION_DISABLED = 2
    DISABLED_BY_ADMIN = 16
    DISABLED_BY_CLIENT = 64


class DomainState(TypedDict):
    domain: str
    status: str


class DomainQueryResult(TypedDict):
    host: str
    id: str
    name: str
    username: str
    userlogin: str
    domains: List[str]
    domain_states: List[DomainState]
    is_space_overused: bool
    subscription_size_mb: int
    subscription_status: str


STATUS_MAPPING = {
    DomainStatus.ONLINE: "online",
    DomainStatus.SUBSCRIPTION_DISABLED: "subscription_is_disabled",
    DomainStatus.DISABLED_BY_ADMIN: "domain_disabled_by_admin",
    DomainStatus.DISABLED_BY_CLIENT: "domain_disabled_by_client",
}


def is_valid_domain(domain_name: str) -> bool:
    if "." in domain_name:
        return 3 <= len(domain_name) <= 63 and bool(
            re.match(DOMAIN_REGEX_PATTERN_STRICT, domain_name)
        )
    else:
        return 3 <= len(domain_name) <= 63 and bool(
            re.match(DOMAIN_REGEX_PATTERN_PARTIAL, domain_name)
        )


def build_query(domain_to_find: str) -> str:
    """
    Builds a SQL query string to search for domain information.
    Compatible with MySQL 5.7.

    Args:
        domain_to_find (str): Domain name pattern to search for

    Returns:
        str: Complete SQL query string
    """
    return f"""
    SELECT 
        base.subscription_id AS result,
        (SELECT name FROM domains WHERE id = base.subscription_id) AS name,
        (SELECT pname FROM clients WHERE id = base.cl_id) AS username,
        (SELECT login FROM clients WHERE id = base.cl_id) AS userlogin,
        (SELECT GROUP_CONCAT(CONCAT(d2.name, ':', d2.status) SEPARATOR ',')
        FROM domains d2 
        WHERE base.subscription_id IN (d2.id, d2.webspace_id)) AS domains,
        (SELECT overuse FROM domains WHERE id = base.subscription_id) as is_space_overused,
        (SELECT ROUND(real_size/1024/1024) FROM domains WHERE id = base.subscription_id) as subscription_size_mb,
        (SELECT status FROM domains WHERE id = base.subscription_id) as subscription_status
    FROM (
        SELECT 
            CASE 
                WHEN webspace_id = 0 THEN id 
                ELSE webspace_id 
            END AS subscription_id,
            cl_id,
            name
        FROM domains 
        WHERE name LIKE '{domain_to_find}'
    ) AS base;
    """


def get_status_string(status_code: int) -> str:
    """Convert numeric status code to string representation."""
    try:
        domain_status = DomainStatus(status_code)
        return STATUS_MAPPING.get(domain_status, "unknown_status")
    except ValueError:
        return "unknown_status"


def parse_domain_states(domain_states_str: str) -> List[DomainState]:
    """Parse domain states string into list of dictionaries."""
    if not domain_states_str:
        return []

    domain_states = []
    for domain_status in domain_states_str.split(","):
        try:
            domain, status = domain_status.split(":")
            status_code = int(status)
            domain_states.append(
                {"domain": domain, "status": get_status_string(status_code)}
            )
        except (ValueError, IndexError):
            continue
    return domain_states


def parse_answer(answer) -> DomainQueryResult:
    result_lines = answer["stdout"].strip().split("\n")[0].split("\t")

    domain_states = parse_domain_states(result_lines[4])

    result = DomainQueryResult(
        host=answer["host"],
        id=result_lines[0],
        name=result_lines[1],
        username=result_lines[2],
        userlogin=result_lines[3],
        domains=[state["domain"] for state in domain_states],
        domain_states=domain_states,
        is_space_overused=result_lines[5].lower() == "true",
        subscription_size_mb=int(result_lines[6]),
        subscription_status=get_status_string(int(result_lines[7])),
    )

    return result


def query_domain_info(domain_name: str, verbose_flag=True, partial_search=False):
    if not is_valid_domain(domain_name):
        raise ValueError("Input string should be a valid domain name.")

    query = (
        build_query(domain_name)
        if not partial_search
        else build_query(domain_name + "%")
    )

    answers = ase.batch_ssh_command_result(
        PLESK_SERVER_LIST,
        f'plesk db -Ne \\"{query}\\"',
        verbose=verbose_flag,
    )
    results = [parse_answer(answer) for answer in answers if answer["stdout"]]
    return results
