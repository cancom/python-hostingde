class ApiException(Exception):
    """
    The client throws an API exception, whenever the error was unknown. Details are included in the exception.
    """

    def __init__(self, details: dict, *args: list, **kwargs: dict) -> None:
        super().__init__(args, kwargs)
        self.details = details

    def __str__(self) -> str:
        return "\n".join([f"{error.get('text')}" for error in self.details.get('errors', [])])


class ClientException(Exception):
    pass
