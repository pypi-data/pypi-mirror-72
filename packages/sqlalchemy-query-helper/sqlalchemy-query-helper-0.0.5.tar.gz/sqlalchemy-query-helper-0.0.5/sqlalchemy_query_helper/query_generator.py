import datetime
from sqlalchemy import inspect, or_, and_
from sqlalchemy.orm import contains_eager


op_mapping = {
    "eq": lambda attr, value: attr == value,
    "neq": lambda attr, value: attr != value,
    "gt": lambda attr, value: attr > value,
    "gte": lambda attr, value: attr >= value,
    "lt": lambda attr, value: attr < value,
    "lte": lambda attr, value: attr <= value,
}


def generate_query(session, model, raw_query):
    query, _filters = _generate_query(model, session.query(model), raw_query)
    for f in _filters:
        query = query.filter(f)
    return query


def _generate_query(model, query, raw_query, parent=None):
    inst = inspect(model)
    filters = []
    ors = raw_query.get("or")
    ands = raw_query.get("and")
    if ors is not None or ands is not None:
        clauses = ors if ors is not None else ands
        clause_filters = []
        for clause in clauses:
            query, _filters = _generate_query(model, query, clause, parent=parent)
            clause_filters.extend(_filters)
        if ors is not None:
            filters.append(or_(*clause_filters).self_group())
        else:
            filters.append(and_(*clause_filters).self_group())
    for c_attr in inst.mapper.column_attrs:
        prop = c_attr.key
        if prop in raw_query:
            simple_query = raw_query[prop]
            operation = op_mapping[simple_query["op"]]
            value = simple_query["value"]
            if c_attr.columns[0].type.python_type == datetime.datetime and isinstance(
                simple_query["value"], str
            ):
                value = datetime.datetime.fromisoformat(value)
            filters.append(operation(getattr(model, prop), simple_query["value"]))
    for r_attr in inst.mapper.relationships:
        prop = r_attr.key
        if prop in raw_query:
            query = query.join(getattr(model, prop))
            if parent is None:
                parent = contains_eager(getattr(model, prop))
            else:
                parent = parent.contains_eager(getattr(model, prop))
            query = query.options(parent)
            query, _filters = _generate_query(
                r_attr.entity.class_, query, raw_query[prop], parent=parent
            )
            filters.extend(_filters)

    return query, filters
