<p align="center">
  <img src="docs/image.png" alt="python-forge banner">
</p>

<br>

# Python Forge

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-v0.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)

> Forge your ideas. Build better Python projects.

Python Forge is a lightweight CLI tool to scaffold Python projects quickly, consistently, and professionally.

It generates ready-to-use project structures from YAML templates, with optional virtual environment creation and Git initialization.

---

## Philosophy

Python Forge is designed to be:

- Simple
- Fast
- CLI-first
- Template-driven
- Useful for real Python engineering projects

It is not a heavy framework.  
It is a focused scaffolding tool for starting clean Python projects without repeating the same setup work manually.

---

## Requirements

- Python 3.10+
- PyYAML
- Git optional, only required if Git initialization is enabled

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Minoiu-Mihai/python-forge.git
cd python-forge
pip install -r requirements.txt
```

---

## Quick Start

Create a professional Python engineering project:

```bash
python forge.py create my_project python_engineering --python 3.12
```

This will:

- Create the project structure
- Generate folders and starter files
- Create a virtual environment
- Initialize a Git repository
- Create an initial commit

By default, the generated project is created next to the `python-forge` repository.

Example layout:

```text
workspace/
├── python-forge/
└── my_project/
```

---

## Basic Usage

```bash
python forge.py create <project_name> <template> [options]
```

Example:

```bash
python forge.py create tracker_benchmark python_engineering
```

Create a project without virtual environment or Git:

```bash
python forge.py create demo_project basic --no-venv --no-git
```

Create a project in a specific directory:

```bash
python forge.py create demo_project basic --output-dir D:\Projects
```

On Linux/macOS:

```bash
python forge.py create demo_project basic --output-dir ~/Projects
```

---

## Options

| Option | Description |
|---|---|
| `--python VERSION` | Select Python version for the virtual environment, for example `3.12` |
| `--no-venv` | Skip virtual environment creation |
| `--no-git` | Skip Git initialization and initial commit |
| `--force` | Apply the template to an existing project without confirmation |
| `--output-dir PATH` | Choose where the project will be created |

---

## Templates

### Built-in templates

| Template | Purpose |
|---|---|
| `basic` | Minimal Python project |
| `package` | Installable Python package structure |
| `cli` | Python command-line application |
| `computer_vision` | Computer vision experiment/project structure |
| `python_engineering` | Professional Python engineering project for tools, pipelines, experiments, and technical validation |

---

## Recommended Template: `python_engineering`

The `python_engineering` template is designed for technical Python projects such as:

- Computer vision utilities
- Tracking and perception experiments
- Data processing tools
- Benchmarking scripts
- Engineering validation tools
- CLI-based technical workflows
- Reproducible experiments
- Robotics/perception helper tools

Generated structure:

```text
my_project/
├── .vscode/
│   └── settings.json
├── configs/
│   ├── default.yaml
│   └── experiments/
│       └── example_experiment.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   ├── samples/
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── usage.md
│   ├── experiments.md
│   └── decisions.md
├── notebooks/
├── outputs/
│   ├── figures/
│   ├── logs/
│   ├── reports/
│   └── runs/
├── scripts/
│   ├── bootstrap.py
│   ├── benchmark.py
│   ├── prepare_data.py
│   └── run_demo.py
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── logging_utils.py
│       ├── core/
│       ├── io/
│       ├── metrics/
│       ├── processing/
│       ├── utils/
│       └── vision/
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
├── pyrightconfig.json
├── Makefile
├── .env.example
├── .gitignore
└── README.md
```

---

## Project Names and Package Names

Python Forge supports separate project and package naming.

For example:

```bash
python forge.py create my-awesome-project python_engineering
```

The generated project folder will be:

```text
my-awesome-project/
```

But the Python package will be normalized as:

```text
src/my_awesome_project/
```

This avoids invalid Python imports caused by dashes, spaces, or unsupported characters.

Example import:

```python
from my_awesome_project.config import load_config
```

---

## Working with the Generated Project

After creating a project:

```bash
cd ../my_project
```

Activate the virtual environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

Install the project in editable mode:

```bash
python -m pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run the generated CLI:

```bash
my_project --config configs/default.yaml
```

Run a script directly:

```bash
python scripts/benchmark.py
```

The `python_engineering` template includes a small `scripts/bootstrap.py` helper so scripts can import from `src/` without requiring an editable install during early development.

---

## VS Code Support

The `python_engineering` template includes:

```text
.vscode/settings.json
pyrightconfig.json
```

These files help VS Code and Pylance resolve imports from the `src/` layout.

Recommended workflow:

```bash
cd ../my_project
code .
```

Open VS Code from the generated project root so the editor detects:

- `src/` imports
- test configuration
- virtual environment path
- Pyright/Pylance configuration

---

## Custom Templates

You can provide your own YAML template file:

```bash
python forge.py create my_project path/to/template.yaml
```

A custom template should define a top-level `template` entry:

```yaml
template:
  description: Custom project structure.

  structure:
    folders:
      - src
      - tests

    files:
      README.md: |
        # {{ project_name }}

        Custom project.

      src/__init__.py: ""

      tests/test_main.py: |
        def test_example():
            assert True
```

Supported template variables:

| Variable | Description |
|---|---|
| `{{ project_name }}` | Original project name passed by the user |
| `{{ package_name }}` | Python-safe normalized package name |
| `{{ venv_python_path }}` | Platform-specific virtual environment interpreter path for VS Code |

---

## Example Output

```text
INFO | Using built-in template: python_engineering
INFO | Template description: Professional Python engineering project for tools, pipelines, experiments, and technical validation.
INFO | Creating project: my_project.
INFO | Package name: my_project
INFO | Target path: D:\Workspace\my_project
INFO | Creating Folders:
          - .vscode
          - configs
          - configs/experiments
          - data/raw
          - data/processed
          - data/samples
          - docs
          - notebooks
          - scripts
          - src/my_project
          - tests/unit
          - tests/integration
          - outputs/figures
          - outputs/logs
          - outputs/reports
          - outputs/runs
INFO | Creating Files:
          - README.md
          - pyproject.toml
          - pyrightconfig.json
          - .vscode/settings.json
          - .gitignore
          - .env.example
          - Makefile
INFO | Creating virtual environment...
INFO | Virtual environment created.
INFO | Initializing git repository...
INFO | Initial commit created.

========== SUMMARY ==========
INFO | Project: my_project
INFO | Location: D:\Workspace\my_project
INFO | Template: python_engineering
INFO | Venv: created (Python 3.12)
INFO | Git: initialized
=============================
```

---

## Notes

### Virtual environment

Python Forge currently creates virtual environments using the selected Python version.

Example:

```bash
python forge.py create my_project python_engineering --python 3.12
```

Skip virtual environment creation:

```bash
python forge.py create my_project python_engineering --no-venv
```

### Git

By default, Python Forge initializes a Git repository and creates an initial commit.

Skip Git initialization:

```bash
python forge.py create my_project python_engineering --no-git
```

### Existing projects

If the target project already exists, Python Forge asks for confirmation before applying the template.

Use `--force` to skip the confirmation:

```bash
python forge.py create my_project python_engineering --force
```

Existing files are not overwritten.

---

## Features

- YAML-based project templates
- Built-in templates
- Custom template support
- Python-safe package name generation
- Optional virtual environment creation
- Optional Git initialization
- Smart incremental updates without overwriting existing files
- VS Code/Pylance support for `src/` layout
- CLI-first workflow
- Output directory selection with `--output-dir`

---

## Current Limitations

- The tool is still a single-file CLI script.
- Virtual environment creation currently depends on the available Python launcher/interpreter setup.
- Existing files are skipped, not overwritten.
- `--force` skips confirmation but does not overwrite files.
- The project is not yet packaged as an installable CLI.
- Remote templates are not supported yet.

---

## Roadmap

### v0.2

- [ ] `--version` flag
- [ ] Dry-run mode
- [ ] Template validation
- [ ] Better error handling for invalid YAML
- [ ] Improve cross-platform virtual environment creation
- [ ] Rename or refine `--force` behavior

---

## Contributing

Feel free to open issues or submit pull requests.

This project is evolving and feedback is welcome.

---

## License

MIT