"""ElasticSearch initialization."""

from elasticsearch import AsyncElasticsearch

from happy.core.config import Settings, get_settings

settings: Settings = get_settings()
host: str = (
    f"https://{settings.elasticsearch_host}:{settings.elasticsearch_port}"
)

elasticsearch: AsyncElasticsearch = AsyncElasticsearch(
    hosts=[host],
    basic_auth=(
        settings.elasticsearch_username,
        settings.elasticsearch_password,
    ),
    verify_certs=False,
)
