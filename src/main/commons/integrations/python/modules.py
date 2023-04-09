

class DynamicImport:
    @staticmethod
    def iter_namespace(ns_pkg):
        # Specifying the second argument (prefix) to iter_modules makes the
        # returned name an absolute name instead of a relative one. This allows
        # import_module to work without having to do additional modification to
        # the name.
        #
        # Source: https://packaging.python.org/guides/creating-and-discovering-plugins/
        import pkgutil

        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    # noinspection PyUnresolvedReferences
    @staticmethod
    def run_module(path: str):
        import importlib.util

        module_spec = importlib.util.spec_from_file_location("plugin", path)
        module_instance = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module_instance)

        return module_instance

