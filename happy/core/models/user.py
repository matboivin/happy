"""User model."""

from pydantic import BaseModel


class User(BaseModel):
    """A user.

    Attributes
    ----------
    id : int
        The user ID.
    username : str
        The username.

    """

    id: int
    username: str
