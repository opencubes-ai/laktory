from laktory.models.base import BaseModel
from laktory.models.resources import Resources


class ServicePrincipal(BaseModel, Resources):
    display_name: str
    application_id: str = None
    allow_cluster_create: bool = False
    groups: list[str] = []
    roles: list[str] = []

    # ----------------------------------------------------------------------- #
    # Resources Engine Methods                                                #
    # ----------------------------------------------------------------------- #

    def deploy_with_pulumi(self, name=None, groups=None, **kwargs):
        from laktory.resourcesengines.pulumi.serviceprincipal import PulumiServicePrincipal
        return PulumiServicePrincipal(name=name, service_principal=self, groups=groups, **kwargs)
