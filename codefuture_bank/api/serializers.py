from rest_framework.serializers import Serializer, BooleanField, CharField


class BaseSerializer(Serializer):
    def __init__(self, **kwargs):
        super().__init__()
        status = BooleanField()
        message = CharField(max_length=150)



