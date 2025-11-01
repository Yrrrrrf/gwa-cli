"""Configuration models for the GWA CLI tool."""

from pydantic import BaseModel, Field
from typing import Optional


class ProjectConfig(BaseModel):
    """Configuration for project generation."""

    project_name: str = Field(
        ...,
        description="Name of the project to create",
        pattern=r"^[a-zA-Z][a-zA-Z0-9_-]*$",  # Alphanumeric, underscore, hyphen, starting with letter
        min_length=1,
        max_length=100,
    )
    description: str = Field("A new project", description="Description of the project")
    author: Optional[str] = Field(None, description="Author of the project")
    template_url: str = Field(
        "https://github.com/rust-cli/default-template",
        description="Git URL of the template to use for generation",
    )
    output_dir: str = Field(
        ".", description="Directory where the project will be created"
    )
    force: bool = Field(False, description="Force overwrite existing directory")
    clone_depth: Optional[int] = Field(
        None, description="Git clone depth (shallow clone)"
    )
    additional_params: dict = Field(
        default_factory=dict, description="Additional template parameters"
    )

    class Config:
        """Pydantic configuration."""

        extra = "forbid"  # Don't allow extra fields
