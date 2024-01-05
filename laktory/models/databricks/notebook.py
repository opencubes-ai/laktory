import os
from typing import Any
from typing import Literal
from typing import Union
from pydantic import model_validator
from laktory.models.basemodel import BaseModel
from laktory.models.resources.pulumiresource import PulumiResource
from laktory.models.databricks.accesscontrol import AccessControl
from laktory.models.databricks.permissions import Permissions


class Notebook(BaseModel, PulumiResource):
    """
    Databricks Notebook

    Attributes
    ----------
    access_controls:
        List of notebook access controls
    dirpath:
        Workspace directory containing the notebook. Filename will be assumed to be the same as local filepath. Used
        if path is not specified.
    language:
         Notebook programming language
    path:
        Workspace filepath for the notebook
    source:
        Path to notebook in source code format on local filesystem.

    Examples
    --------
    ```py
    from laktory import models

    notebook = models.Notebook(
        source="./notebooks/pipelines/dlt_brz_template.py",
    )
    print(notebook.path)
    #> /pipelines/dlt_brz_template.py

    notebook = models.Notebook(source="./notebooks/create_view.py", dirpath="/views/")
    print(notebook.path)
    #> /views/create_view.py
    ```
    """

    access_controls: list[AccessControl] = []
    dirpath: str = None
    language: Literal["SCALA", "PYTHON", "SQL", "R"] = None
    path: str = None
    source: str

    @property
    def filename(self) -> str:
        """Notebook file name"""
        return os.path.basename(self.source)

    @model_validator(mode="after")
    def default_path(self) -> Any:
        if self.path is None:
            if self.dirpath:
                self.path = f"{self.dirpath}{self.filename}"

            elif "/notebooks/" in self.source:
                self.path = "/.laktory/" + self.source.split("/notebooks/")[-1]

        return self

    # ----------------------------------------------------------------------- #
    # Resource Properties                                                     #
    # ----------------------------------------------------------------------- #

    @property
    def resource_key(self) -> str:
        """Notebook resource key"""
        key = self.path
        key = key.replace("/", "-")
        key = key.replace("\\", "-")
        key = key.replace(".", "-")
        for i in range(5):
            if key.startswith("-"):
                key = key[1:]
        return key

    @property
    def resources(self) -> list[PulumiResource]:
        if self.resources_ is None:
            self.resources_ = [
                self,
            ]
            if self.access_controls:
                self.resources_ += [
                    Permissions(
                        resource_name=f"permissions-{self.resource_name}",
                        access_controls=self.access_controls,
                        notebook_path=f"${{resources.{self.resource_name}.path}}",
                    )
                ]

        return self.resources_

    # ----------------------------------------------------------------------- #
    # Pulumi Properties                                                       #
    # ----------------------------------------------------------------------- #

    @property
    def pulumi_resource_type(self) -> str:
        return "databricks:Notebook"

    @property
    def pulumi_cls(self):
        import pulumi_databricks as databricks

        return databricks.Notebook

    @property
    def pulumi_excludes(self) -> Union[list[str], dict[str, bool]]:
        return ["access_controls", "dirpath"]
