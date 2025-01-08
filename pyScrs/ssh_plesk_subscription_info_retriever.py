from host_lists import PLESK_SERVER_LIST
import ssh_async_executor as ase
import re

DOMAIN_REGEX_PATTERN_STRICT = (
    r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,8}$"
)

DOMAIN_REGEX_PATTERN_PARTIAL = r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))$"


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
    return f"""
    WITH target AS (
        SELECT 
            CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS subscription_id,
            cl_id,
            name
        FROM domains
        WHERE name LIKE '{domain_to_find}'
    ),
    user_info AS (
        SELECT 
            id,
            pname,
            login
        FROM clients
    )
    SELECT 
        t.subscription_id AS result,
        t.name,
        (SELECT pname FROM user_info WHERE id=t.cl_id) AS username,
        (SELECT login FROM user_info WHERE id=t.cl_id) AS userlogin,
        (SELECT GROUP_CONCAT(CONCAT(d2.name, ':', d2.status) SEPARATOR ',')
         FROM domains d2 
         WHERE t.subscription_id IN (d2.id, d2.webspace_id)) AS domains,
         (SELECT overuse FROM domains WHERE id=t.subscription_id) as is_space_overused,
         (SELECT round(real_size/1024/1024) FROM domains WHERE id=t.subscription_id) as subscription_size_mb,
         (SELECT status FROM domains WHERE id=t.subscription_id) as subscription_status
    FROM target t;
    """


def parse_answer(answer) -> dict:
    status_mapping = {
        0: "online",
        2: "subscription_is_disabled",
        16: "domain_disabled_by_admin",
        64: "domain_disabled_by_client",
    }

    result_lines = answer["stdout"].strip().split("\n")[0].split("\t")

    domain_states_list = [
        {
            "domain": domain_status.split(":")[0],
            "status": status_mapping.get(
                int(domain_status.split(":")[1]), "unknown_status"
            ),
        }
        for domain_status in result_lines[4].split(",")
    ]

    domains_list = [entry["domain"] for entry in domain_states_list]

    parsed_answer = {
        "host": answer["host"],
        "id": result_lines[0],
        "name": result_lines[1],
        "username": result_lines[2],
        "userlogin": result_lines[3],
        "domains": domains_list,
        "domain_states": domain_states_list,
        "is_space_overused": True if result_lines[5] == "true" else False,
        "subscription_size_mb": int(result_lines[6]),
        "subscription_status": status_mapping.get(
            int(result_lines[7]), "unknown_status"
        ),
    }
    return parsed_answer


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
