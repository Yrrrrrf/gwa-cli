"""Textual TUI application for GWA project creation."""

from typing import Dict, Any

import textual
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input, Label, Switch, Static


class GwaCreator(App):
    """A Textual application for interactive project creation."""

    # Reactive variables to track form state
    project_name = reactive("")
    description = reactive("A new project")
    author = reactive("")
    template_url = reactive("https://github.com/rust-cli/default-template")
    output_dir = reactive(".")
    force_overwrite = reactive(False)
    use_shallow_clone = reactive(False)
    clone_depth = reactive(1)

    CSS_PATH = None  # We'll define CSS inline

    def __init__(self):
        super().__init__()
        self.title = "GWA Project Creator"
        self.sub_title = "Interactive Project Generation"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

        with Container(id="main_container"):
            yield Static("GWA Project Creator", classes="title")

            # Project Name Input
            yield Label("Project Name:", id="project_name_label")
            yield Input(
                placeholder="Enter project name (letters, numbers, _, -)",
                id="project_name_input",
                validators=[textual.validation.Length(minimum=1)],
            )

            # Description Input
            yield Label("Description:", id="description_label")
            yield Input(
                value="A new project",
                placeholder="Enter project description",
                id="description_input",
            )

            # Author Input
            yield Label("Author (optional):", id="author_label")
            yield Input(placeholder="Enter author name", id="author_input")

            # Template URL Input
            yield Label("Template URL:", id="template_url_label")
            yield Input(
                value="https://github.com/rust-cli/default-template",
                placeholder="Enter git URL of template",
                id="template_url_input",
            )

            # Output Directory Input
            yield Label("Output Directory:", id="output_dir_label")
            yield Input(
                value=".", placeholder="Enter output directory", id="output_dir_input"
            )

            # Force Overwrite Switch
            with Horizontal(id="force_container"):
                yield Label("Force Overwrite:", id="force_label")
                yield Switch(value=False, id="force_switch")

            # Shallow Clone Options
            with Horizontal(id="shallow_container"):
                yield Label("Use Shallow Clone:", id="shallow_label")
                yield Switch(value=False, id="shallow_switch")

            with Horizontal(id="depth_container"):
                yield Label("Clone Depth:", id="depth_label")
                yield Input(
                    value="1",
                    placeholder="Enter clone depth",
                    id="depth_input",
                    disabled=True,
                )

            # Action Buttons
            with Horizontal(id="buttons_container"):
                yield Button("Cancel", variant="error", id="cancel_button")
                yield Button("Create Project", variant="success", id="create_button")

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        # Disable depth input initially since shallow clone is off
        self.query_one("#depth_input").disabled = not self.use_shallow_clone

        # Set up reactive watchers
        self.watch(
            self.query_one("#project_name_input", expect_type=Input),
            "value",
            self._on_project_name_changed,
        )

        self.watch(
            self.query_one("#description_input", expect_type=Input),
            "value",
            self._on_description_changed,
        )

        self.watch(
            self.query_one("#author_input", expect_type=Input),
            "value",
            self._on_author_changed,
        )

        self.watch(
            self.query_one("#template_url_input", expect_type=Input),
            "value",
            self._on_template_url_changed,
        )

        self.watch(
            self.query_one("#output_dir_input", expect_type=Input),
            "value",
            self._on_output_dir_changed,
        )

    def _on_project_name_changed(self, value: str) -> None:
        """Update the reactive variable when project name changes."""
        self.project_name = value

    def _on_description_changed(self, value: str) -> None:
        """Update the reactive variable when description changes."""
        self.description = value

    def _on_author_changed(self, value: str) -> None:
        """Update the reactive variable when author changes."""
        self.author = value

    def _on_template_url_changed(self, value: str) -> None:
        """Update the reactive variable when template URL changes."""
        self.template_url = value

    def _on_output_dir_changed(self, value: str) -> None:
        """Update the reactive variable when output directory changes."""
        self.output_dir = value

    @on(Switch.Changed, "#force_switch")
    def _on_force_switch_changed(self, event: Switch.Changed) -> None:
        """Handle changes to the force overwrite switch."""
        self.force_overwrite = event.value

    @on(Switch.Changed, "#shallow_switch")
    def _on_shallow_switch_changed(self, event: Switch.Changed) -> None:
        """Handle changes to the shallow clone switch."""
        self.use_shallow_clone = event.value
        # Enable/disable depth input based on shallow clone setting
        depth_input = self.query_one("#depth_input", expect_type=Input)
        depth_input.disabled = not event.value

    @on(Input.Changed, "#depth_input")
    def _on_depth_input_changed(self, event: Input.Changed) -> None:
        """Handle changes to the clone depth input."""
        try:
            # Only update if the value is a valid integer
            value = int(event.value)
            if value > 0:
                self.clone_depth = value
        except ValueError:
            # If it's not a valid integer, keep the previous value
            pass

    @on(Button.Pressed, "#cancel_button")
    def _on_cancel_button(self) -> None:
        """Handle cancel button press."""
        self.exit(None)

    @on(Button.Pressed, "#create_button")
    def _on_create_button(self) -> None:
        """Handle create button press - collect form data and exit."""
        # Validate project name
        project_name_input = self.query_one("#project_name_input", expect_type=Input)
        if not self._is_valid_project_name(self.project_name):
            project_name_input.styles.border = ("round", "red")
            return

        # Collect form data into a dictionary
        config = {
            "project_name": self.project_name,
            "description": self.description,
            "author": self.author if self.author.strip() else None,
            "template_url": self.template_url,
            "output_dir": self.output_dir,
            "force": self.force_overwrite,
            "clone_depth": self.clone_depth if self.use_shallow_clone else None,
            "additional_params": {},
        }

        self.exit(config)

    def _is_valid_project_name(self, name: str) -> bool:
        """Validate project name format."""
        if not name:
            return False
        # Check that name starts with a letter and only contains alphanumeric, underscore, or hyphen
        import re

        return bool(re.match(r"^[a-zA-Z][a-zA-Z0-9_-]*$", name))

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes for validation feedback."""
        # Provide real-time validation feedback for project name
        if event.input.id == "project_name_input":
            if self._is_valid_project_name(event.value):
                event.input.styles.border = ("round", "green")
            else:
                event.input.styles.border = ("round", "red")


def run_tui() -> Dict[str, Any]:
    """Run the TUI and return the configuration dictionary."""
    app = GwaCreator()
    result = app.run()

    # If user cancelled, exit the program
    if result is None:
        import sys

        sys.exit(0)

    return result


if __name__ == "__main__":
    run_tui()
