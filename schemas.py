from pydantic import BaseModel, ConfigDict, Field

class URLCreate(BaseModel):
    url: str = Field(min_length=1)

class URLResponse(BaseModel):
    short_url: str = Field(min_length=1)
    long_url: str = Field(min_length=1)