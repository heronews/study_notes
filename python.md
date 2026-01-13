# mongodb etc
```
Field(validation_alias=AliasChoices("id", "_id"))

pipeline = [
    {
        "$set": {
            key: {"$mergeObjects": ["$key", new_value]}
        }
    }
]
```
# numpy structured arrays
```
arr = numpy.frombuffer(
    buffer,
    [
        ("x", "f4"),
        ("y", "f4"),
        ("z", "f4"),
    ],
)
```
