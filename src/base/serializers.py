from rest_framework.serializers import SerializerMethodField, ModelSerializer
from base.models import BaseModel


class ReadWriteSerializerMethodField(SerializerMethodField):
    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        self.read_only = False
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {f'{self.field_name}_id': data}


class BaseModelSerializer(ModelSerializer):
    class Meta:
        model = BaseModel
        abstract = True


class DynamicFieldsModelSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", None)
        rw_method_fields = kwargs.pop("rw_method_fields", None)
        r_method_fields = kwargs.pop("r_method_fields", None)
        related_fields = kwargs.pop("related_fields", None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude_fields:
            for field_name in exclude_fields:
                self.fields.pop(field_name)

        if rw_method_fields:
            for name in rw_method_fields:
                self.fields[name] = ReadWriteSerializerMethodField(
                    source=f"get_{name}")

        if r_method_fields:
            for name in r_method_fields:
                self.fields[name] = SerializerMethodField(source=f"get_{name}")

        if related_fields:
            for item in related_fields:
                name = item.pop("name")
                serializer = item.pop("serializer")
                self.fields[name] = serializer
