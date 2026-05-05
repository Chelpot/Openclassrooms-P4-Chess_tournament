class Round:

    def __init__(self, name, starting_date_hour, ending_date_hour, matches=None, id=None):
        self.name = name
        self.starting_date_hour = starting_date_hour
        self.ending_date_hour = ending_date_hour
        self.matches = matches if matches is not None else []
        self.id = id

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            starting_date_hour=data["starting_date_hour"],
            ending_date_hour=data["ending_date_hour"],
            matches=data.get("matches", []),
            id=data.get("id")
        )
