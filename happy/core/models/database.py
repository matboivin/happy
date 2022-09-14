"""ElasticSearch initialization."""

import os

from dotenv import load_dotenv
from elasticsearch import AsyncElasticsearch

load_dotenv()

elasticsearch: AsyncElasticsearch = AsyncElasticsearch(
    hosts=[os.getenv("ELASTICSEARCH_HOSTS")],
    http_auth=(
        os.getenv("ELASTICSEARCH_USERNAME"),
        os.getenv("ELASTICSEARCH_PASSWORD"),
    ),
)
