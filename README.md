
<p align="center">
  <img src="https://raw.githubusercontent.com/Yrrrrrf/gwa/main/resources/img/gwa-no-bg.png" alt="General Web App Icon" width="128" height="128">
</p>

<h1 align="center">
GWA Scaffolder
</h1>

<p align="center">
  A lightning-fast, interactive CLI for creating new <a href="https://github.com/Yrrrrrf/gwa">GWA</a> projects.
</p>

<p align="center">
  <a href="https://github.com/Yrrrrrf/gwa-create/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://www.rust-lang.org/"><img src="https://img.shields.io/badge/made%20with-Rust-orange.svg"></a>
</p>

`gwa-create` is the official command-line tool for scaffolding a new [**General Web App (GWA)**](https://github.com/Yrrrrrf/gwa) project. It provides an interactive experience to configure your new project, allowing you to select components, define names, and set up database credentials before generating all the necessary files from the GWA template.

This tool handles all the heavy lifting, so you can go from an empty directory to a fully structured, ready-to-run, full-stack application in seconds.

## ✨ Features

- **Interactive Mode:** A guided, user-friendly process to configure every aspect of your new project.
- **Modular Component Selection:** Choose to include the Backend (FastAPI), Frontend (SvelteKit + Tauri), or both.
- **Intelligent Defaults:** Sensible defaults are provided for all settings, speeding up creation.
- **Fast-Track Mode:** Skip all prompts with a `--yes` flag for rapid, non-interactive project generation.
- **Powered by Rust:** Fast, reliable, and packaged as a single native binary.

## 🚀 Getting Started

### Prerequisites

You must have [Rust and Cargo](https://www.rust-lang.org/tools/install) installed on your system to build and install `gwa-create`.

### Installation

You can install the `gwa` binary directly from this source repository using `cargo`.

This command will build the project in release mode and place the `gwa` executable in your Cargo binary path (`~/.cargo/bin/`), making it available system-wide.
```sh
cargo install gwa-create
```

**Verify the installation:**
```sh
gwa --version
```

## 🛠️ Usage

The primary command is `gwa create`.

### Interactive Creation (Recommended)

To start the interactive setup wizard, simply run:

```sh
gwa create <your-project-name>
```

The CLI will guide you through a series of questions:

-   Project Name (if not provided)
-   Component Selection (Backend / Frontend)
-   Application Identifiers (for Tauri)
-   Database Configuration

After you confirm the summary, it will generate the project in a new directory named `<your-project-name>`.

### Non-Interactive Creation

For automated scripts or quick tests, you can use the `--yes` (`-y`) flag. This will skip all interactive prompts and use the default configuration.

**Note:** In non-interactive mode, the project name is a required argument.

```sh
gwa create my-new-app --yes
```

This will instantly create a new project named `my-new-app` with both backend and frontend components included.

### Command-Line Options

Here are the details for the `create` command:

```
gwa create [OPTIONS] [NAME]
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.