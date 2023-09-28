from string import Template


def load_query(query_path, **kwargs):
    with open(query_path, "r") as fp:
        raw = fp.read()
        query = Template(raw).substitute(kwargs)
        return query
