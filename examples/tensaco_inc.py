# The problem is, I don't want to write all the details for the python object. I want it to have a large set of parameters. Instead, you should just specify the structured and semistructured databases, keys, and callables.

tensaco_inc = Company(
    "tensa_co", "tensa_co.db", tensacode_team=Team(...)
)  # it should accept most of its args as unstructured code inputs and parse them intelligently

tensaco_inc.run

```
$ tensorco run