import json

from rest_framework.status import is_success
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json

from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination


def manage_error(errors, temp_list=[]):
    temp_list_2 = []
    for key, value in errors.items():
        if isinstance(value, dict):
            temp_list.append(handel_json_error(key, manage_error(value)))
            temp_list_2 = temp_list

        elif isinstance(value, list):
            temp_list_2.append(handel_list_error(key, value))

        else:
            temp_list_2.append(handel_list_error(key, value))
    return temp_list_2


def handel_list_error(key, errors: list):
    return {key: default_format(message=errors)}


def handel_json_error(key, errors: dict):
    return {key: default_format(child=errors)}


def default_format(message=None, child=None):
    return {"message": message, "child": child}


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        rendered = json.loads(super(CustomJSONRenderer, self).render(data or [], accepted_media_type, renderer_context))
        response = renderer_context['response']
        errors = []
        error_list = []
        if not is_success(response.status_code):
            if isinstance(rendered, list):
                errors = [handel_list_error(key="errors", errors=rendered)]
            elif isinstance(rendered, str):
                errors = [default_format(rendered)]
            else:
                errors = manage_error(rendered, error_list)

        response_data = {
            'results': rendered if is_success(response.status_code) else [],
            'status': response.status_code,
            'success': is_success(response.status_code),
            'messages': [] if is_success(response.status_code) else errors,
        }
        response = super().render(response_data, accepted_media_type, renderer_context)
        if response_data['status'] == 500:
            print(response_data)
        return response


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_pagination_parameters(self, view):
        if isinstance(getattr(view, 'pagination_class', None), PageNumberPagination):
            return [
                openapi.Parameter('page', in_=openapi.IN_QUERY, description='Page number', type=openapi.TYPE_INTEGER),
                openapi.Parameter('page_size', in_=openapi.IN_QUERY, description='Number of results per page',
                                  type=openapi.TYPE_INTEGER),
            ]
        return []

    def get_default_responses(self, response_serializers):
        responses = super().get_default_responses(response_serializers)
        responses['200'] = openapi.Response(
            description='Success',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'message': openapi.Schema(type=openapi.TYPE_STRING),
                    'data': responses['200'].schema,
                }
            ),
        )
        return responses
