from collections import OrderedDict
from django.conf.urls import url
from rest_framework import routers
from rest_framework.settings import api_settings
from rest_framework.urlpatterns import format_suffix_patterns


class MainRouter(routers.SimpleRouter):

    root_view_name = 'api-root'
    default_schema_renderers = None
    APIRootView = routers.APIRootView
    APISchemaView = routers.SchemaView
    SchemaGenerator = routers.SchemaGenerator

    def __init__(self, *args, **kwargs):
        if 'root_renderers' in kwargs:
            self.root_renderers = kwargs.pop('root_renderers')
        else:
            self.root_renderers = list(api_settings.DEFAULT_RENDERER_CLASSES)
        self.children = []
        super().__init__()

    def register_child(self, router):
        self.children.append(router)

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        route_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = route_name.format(basename=basename)

        for child in self.children:
            route_name = child.routes[0].name
            for prefix, viewset, basename in child.registry:
                api_root_dict[prefix] = route_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = super().get_urls()

        for child in self.children:
            urls.extend(child.urls)

        view = self.get_api_root_view(api_urls=urls)
        root_url = url(r'^$', view, name=self.root_view_name)
        urls.append(root_url)

        urls = format_suffix_patterns(urls)

        return urls


class StandardRouter(routers.DefaultRouter):
    include_root_view = False
    include_format_suffixes = False
