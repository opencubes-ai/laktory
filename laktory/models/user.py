from laktory.models.base import BaseModel
from laktory.models.resources import Resources


class User(BaseModel, Resources):
    user_name: str
    display_name: str = None
    workspace_access: bool = True
    groups: list[str] = []
    roles: list[str] = []

    # ----------------------------------------------------------------------- #
    # Resources Engine Methods                                                #
    # ----------------------------------------------------------------------- #

    def deploy_with_pulumi(self, name=None, groups=None, **kwargs):
        from laktory.resourcesengines.pulumi.user import PulumiUser
        return PulumiUser(name=name, user=self, groups=groups, **kwargs)
