from elasticsearch import Elasticsearch
from app.settings import ELASTICSEARCH as ELS


def elastic_conn():
    return Elasticsearch(
        hosts=[f"{ELS['SCHEME']}://{ELS['ADDRESS']}:{ELS['PORT']}"],
        basic_auth=(ELS['USER'], ELS['PASSWD']),
        ca_certs=False,
        verify_certs=False,
        ssl_show_warn=False
    )


mapping = {
    'properties': {
        'agency': {'type': 'integer'},
        'account': {'type': 'integer'},
        'name': {'type': 'text'},
        'age': {'type': 'integer'}
    }
}