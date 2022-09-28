"""User-related service."""

from dataclasses import dataclass

from elastic_transport import ObjectApiResponse
from elasticsearch import AsyncElasticsearch, NotFoundError
from verboselogs import VerboseLogger

from happy.core.logger import init_logger
from happy.core.schemas import User


@dataclass
class UsersService:
    """Class defining the users-related service.

    Attributes
    ----------
    elasticsearch : elasticsearch.AsyncElasticsearch
        The ElasticSearch interface.
    logger : verboselogs.VerboseLogger
        The service logger.
    index : str, optional
        The index name (default: 'users').

    Methods
    -------
    fetch_users()
        Return all the documents from the users index.
    fetch_user(user_id)
        Return the user matching the given ID.
    post_user(user_id, user, exclude_unset = False)
        Post a new user to the users index.

    """

    elasticsearch: AsyncElasticsearch
    logger: VerboseLogger = init_logger("Users Service")
    index: str = "users"

    async def fetch_users(self) -> ObjectApiResponse:
        """Return all the documents from the users index.

        Returns
        -------
        elastic_transport.ObjectApiResponse
            The response object returned by ElasticSearch.

        """
        self.logger.spam("Fetch all from users index.")

        return await self.elasticsearch.search(index=self.index)

    async def fetch_user(self, user_id: int) -> ObjectApiResponse:
        """Return the user matching the given ID.

        Parameters
        ----------
        user_id : int
            The user identifier.

        Returns
        -------
        elastic_transport.ObjectApiResponse
            The response object returned by ElasticSearch.

        Raises
        ------
        FileNotFoundError
            If the user is not found.

        """
        try:
            response: ObjectApiResponse = await self.elasticsearch.get(
                index=self.index, id=user_id
            )
        except NotFoundError as err:
            raise FileNotFoundError(f"User {user_id} not found.") from err

        return response["_source"]

    async def post_user(
        self, user_id: int, user: User, exclude_unset: bool = False
    ) -> ObjectApiResponse:
        """Post a new user to the users index.

        Parameters
        ----------
        user_id : int
            The user identifier.
        user : User
            The document to post.
        exclude_unset : bool, optional
            Whether to remove unset attributes from dict (default: False).

        Returns
        -------
        elastic_transport.ObjectApiResponse
            The response object returned by ElasticSearch.

        Raises
        ------
        elasticsearch.BadRequestError
            If there was something wrong in the request.

        """
        self.logger.spam(f"Post user {user_id} to users index.")

        return await self.elasticsearch.update(
            index=self.index,
            id=user_id,
            body={
                "doc": user.dict(exclude_unset=exclude_unset),
                "doc_as_upsert": True,
            },
        )
