# SQLAlchemy query helper

## Usage

```python
class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    timestamp = Column(DateTime)
    addresses = relationship("Address")

class Address(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))

from sqlalchemy_query_helper.query_generator import generate_query

# it will return sql alchemy query object
query=generate_query(session,User,{
    "name":{"op":"eq","value":"john"},
    "addresses":{"title":{"op":"neq":"value":"new york city"}}
})
# this query is equivalent to below
"""
SELECT user.*,address.* from user
join address on address.user_id=user.id
where user.name='john' and address.title!='new york city'
"""
# notice that it will load joined table if it is in the query.
# There is no select option yet

```

### Available operations

- `eq` (equals)
- `neq` (not equals)
- `gt` (greater than)
- `gte` (greater than equals)
- `lt` (less than)
- `lte` (less than equals)

### More

- Accepts date times as iso format and will convert to python `datetime` automatically.

## Development

- Install `pipenv`

- `make install`

- Make your changes and open PR

## Test

- Install `sqllite3`

- `make test`
