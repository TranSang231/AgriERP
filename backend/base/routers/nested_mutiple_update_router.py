from rest_framework_nested.routers import NestedMixin
from .mutiple_update_router import MutipleUpdateRouter

class NestedMutipleUpdateRouter(NestedMixin, MutipleUpdateRouter):
    """ Create a NestedMutipleUpdateRouter nested within `parent_router`
    Args:

    parent_router: Parent router. Maybe be a MutipleUpdateRouter or another
        NestedMutipleUpdateRouter.

    parent_prefix: The url prefix within parent_router under which the
        routes from this router should be nested.

    lookup:
        The regex variable that matches an instance of the parent-resource
        will be called '<lookup>_<parent-viewset.lookup_field>'
        In the example above, lookup=domain and the parent viewset looks up
        on 'pk' so the parent lookup regex will be 'domain_pk'.
        Default: 'nested_<n>' where <n> is 1+parent_router.nest_count

    """
    pass
