from importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.views import generic


class View(generic.View):
    pass


class Site(object):
    def __init__(self):
        self.view_classes = []

    def get_urls(self):
        from django.apps import apps
        from django.urls import path

        for app_config in apps.get_app_configs():
            if module_has_submodule(app_config.module, "api"):
                module_name = "%s.%s" % (app_config.name, "api")
                import_module(module_name)

        urlpatterns = []

        for view_class in self.view_classes:
            urlpatterns += [
                path(
                    view_class.path,
                    view_class.as_view(),
                    name=view_class.path_name,
                )
            ]

        return urlpatterns

    def register(self, view_class):
        self.view_classes.append(view_class)

    @property
    def urls(self):
        return self.get_urls(), "api", "api"


site = Site()


def register(view_class):
    site.register(view_class)
    return lambda: view_class
