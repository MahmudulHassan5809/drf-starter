from rest_framework.serializers import SerializerMethodField, ModelSerializer
from base.models import BaseModel


class ReadWriteSerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        self.read_only = False
        super(SerializerMethodField, self).__init__(**kwargs)


class BaseModelSerializer(ModelSerializer):
    class Meta:
        model = BaseModel
        abstract = True


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        method_fields = kwargs.pop('method_fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields:
            fields = fields.split(',')
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if method_fields:
            method_fields = method_fields.split(',')
            for name in method_fields:
                self.fields[name] = SerializerMethodField(
                    read_only=True, source=f'get_{name}')
