from typing import Union
from pydantic import Field

from laktory._settings import settings
from laktory.models.base import BaseModel
from laktory.models.producer import Producer


class DataEventHeader(BaseModel):
    """
    Data Event Header

    Attributes
    ----------
    name
        Data event name
    description
        Data event description
    producer
        Data event producer
    events_root
        Root path for all events
    """
    name: str = Field(...)
    description: Union[str, None] = Field(None)
    producer: Producer = Field(None)
    events_root: str = settings.workspace_landing_root + "events/"

    # ----------------------------------------------------------------------- #
    # Paths                                                                   #
    # ----------------------------------------------------------------------- #

    @property
    def event_root(self) -> str:
        """
        Root path for the event, defined as `{events_roots}/{producer_name}/{event_name}/`

        Returns
        -------
        output
            Event path
        """
        producer = ""
        if self.producer is not None:
            producer = self.producer.name + "/"
        v = f"{self.events_root}{producer}{self.name}/"
        return v

    #
    # @field_validator("root_path")
    # def default_root_path(cls, v: str, info: FieldValidationInfo) -> str:
    #     if v is None:
    #         data = info.data
    #         producer = ""
    #         if data.get("producer") is not None:
    #             producer = data["producer"].name + "/"
    #         v = f'{data.get("events_root_path", "")}{producer}{data.get("name", "")}/'
    #     return v
