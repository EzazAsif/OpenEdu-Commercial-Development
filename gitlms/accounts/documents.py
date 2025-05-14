from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import User

# Declare index with analyzers
user_index = Index('users')

user_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
    analysis={
        "analyzer": {
            "autocomplete": {
                "type": "custom",
                "tokenizer": "autocomplete_tokenizer",
                "filter": ["lowercase"]
            },
            "autocomplete_search": {
                "type": "custom",
                "tokenizer": "lowercase"
            }
        },
        "tokenizer": {
            "autocomplete_tokenizer": {
                "type": "edge_ngram",
                "min_gram": 1,
                "max_gram": 20,
                "token_chars": ["letter", "digit"]
            }
        }
    }
)



@registry.register_document
class UserDocument(Document):
    first_name = fields.TextField(analyzer='autocomplete', search_analyzer='autocomplete_search')
    last_name = fields.TextField(analyzer='autocomplete', search_analyzer='autocomplete_search')
    email = fields.TextField(analyzer='autocomplete', search_analyzer='autocomplete_search')

    # Add department and course as keyword or integer fields (depending on mapping)
    department = fields.IntegerField()  # or fields.KeywordField() if you want exact match string
    course = fields.IntegerField()

    class Index:
        name = 'users'
        settings = user_index._settings  # Your existing settings

    class Django:
        model = User
        fields = [
            'id',
            'role',
            'profilepicture',
            'department',
            'course',
        ]

