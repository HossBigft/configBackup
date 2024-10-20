from host_lists import PLESK_SERVER_LIST
import ssh_async_executor as ase


def build_query(domain_to_find: str) -> str:
    return (
        f"SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result "
        f"FROM domains WHERE name LIKE '{domain_to_find}'; "
        f"SELECT name FROM domains WHERE id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{domain_to_find}'); "
        f"SELECT pname, login FROM clients WHERE id=(SELECT cl_id FROM domains WHERE name LIKE '{domain_to_find}'); "
        f"SELECT name FROM domains WHERE webspace_id=(SELECT CASE WHEN webspace_id = 0 THEN id ELSE webspace_id END AS result FROM domains WHERE name LIKE '{domain_to_find}');"
    )


def parse_answer(answer) -> dict:
    stdout_lines = answer["stdout"].strip().split("\n")
    return {
        "host": answer["host"],
        "id": stdout_lines[0],
        "name": stdout_lines[1],
        "username": stdout_lines[2].split("\t")[0],
        "userlogin": stdout_lines[2].split("\t")[1],
        "domains": stdout_lines[3:],
    }


def query_domain_info(domain_to_find: str, verbose_flag=True, partial_search=False):
    query = (
        build_query(domain_to_find)
        if not partial_search
        else build_query(domain_to_find + "%")
    )

    answers = ase.batch_ssh_command_result(
        PLESK_SERVER_LIST,
        f'plesk db -Ne \\"{query}\\"',
        verbose=verbose_flag,
    )

    results = [parse_answer(answer) for answer in answers if answer["stdout"]]
    return results
