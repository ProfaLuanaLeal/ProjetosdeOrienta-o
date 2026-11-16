from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    student_name: str = Field(min_length=1, max_length=150)
    advisor_name: str = Field(min_length=1, max_length=150)
    status: str = Field(default="planned", min_length=1, max_length=30)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    student_name: str | None = Field(default=None, min_length=1, max_length=150)
    advisor_name: str | None = Field(default=None, min_length=1, max_length=150)
    status: str | None = Field(default=None, min_length=1, max_length=30)


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
