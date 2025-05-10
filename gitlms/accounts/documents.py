from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import User

user_index = Index('users')

@registry.register_document
class UserDocument(Document):
    class Index:
        name = 'users'

    class Django:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'contact',
            'role',
            'institute',
            'course',
            'department',
            'profilepicture'
        ]
