from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_settings


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        swagger_settings.DISPLAY_OPERATION_ID = False
        operation_keys = operation_keys or self.operation_keys

        tags = self.overrides.get('tags')
        if not tags:
            tags = [operation_keys[0]]
        if hasattr(self.view, "swagger_tags"):
            tags = self.view.swagger_tags

        return tags
