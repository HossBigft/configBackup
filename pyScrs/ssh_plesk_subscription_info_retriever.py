import json
import re


from host_lists import PLESK_SERVER_LIST
import ssh_async_executor as ase


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
    return f"WITH target AS ( SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS target_id, cl_id FROM domains WHERE name LIKE '{domain_to_find}' ) SELECT JSON_OBJECT( 'subscription_id', t.target_id, 'subscription_name', d.name, 'status', d.status, 'space_overuse', d.overuse, 'user', ( SELECT JSON_OBJECT('name', pname, 'login_id', login) FROM clients WHERE id = t.cl_id ), 'domains', CONCAT('[', COALESCE( GROUP_CONCAT( JSON_OBJECT( 'domain', d2.name, 'status', d2.status ) ), '[]' ), ']') ) AS combined_result FROM target t JOIN domains d ON d.id = t.target_id LEFT JOIN domains d2 ON t.target_id IN (d2.id, d2.webspace_id) GROUP BY t.target_id, d.name, d.status, d.overuse, t.cl_id;"


def parse_answer(answer) -> dict | None:
    try:
        parsed_stdout = json.loads(
            answer["stdout"]
            .replace("\\", "")
            .replace('"[{', "[{")
            .replace('}]"', "}]")
            .replace('"{', "{")
            .replace('}"', "}")
        )
        parsed_answer = {
            "host": answer["host"],
            "id": parsed_stdout["subscription_id"],
            "name": parsed_stdout["subscription_name"],
            "username": parsed_stdout["user"]["name"],
            "userlogin": parsed_stdout["user"]["login_id"],
            "domains": parsed_stdout["domains"],
        }

        return parsed_answer
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing the answer: {e}")
        return None


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
