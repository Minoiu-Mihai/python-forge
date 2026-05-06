import yaml
from pathlib import Path
import subprocess
import logging as l
import argparse
import re
import os



l.basicConfig(
    level= l.INFO,
    format= "%(levelname)s | %(message)s",
)

CONFIG_FILE = "projects.yaml"


def normalize_package_name(project_name):
    package_name = project_name.strip().lower()
    package_name = package_name.replace("-", "_").replace(" ", "_")
    package_name = re.sub(r"[^a-zA-Z0-9_]", "_", package_name)
    
    if package_name and package_name[0].isdigit():
        package_name = f"_{package_name}"
    
    return package_name

def get_venv_python_path():
    
    if os.name == "nt":
        return "${workspaceFolder}/.venv/Scripts/python.exe"
    
    return "${workspaceFolder}/.venv/bin/python"
        

def render_template_text(text, project_name):
    package_name = normalize_package_name(project_name)
    venv_python_path = get_venv_python_path()
    return (
        text
        .replace("{{ project_name }}", project_name)
        .replace("{{ package_name }}", package_name)
        .replace("{{ venv_python_path }}", venv_python_path)
    )

def get_default_py_version():

    try:
        version_catcher = subprocess.run(
        ["py", "-0"],
        check=True,
        capture_output=True,
        text=True, 
        ).stdout.strip().splitlines()

        versions = []

        for line in version_catcher:
            line = line.strip()

            if line.startswith("-V:"):
                version = line.split(":")[1].split()[0]
                versions.append(version)
        if versions:
            versions.sort(key=lambda v: list(map(int, v.split("."))), reverse=True)
            return versions[0]
        else:
            l.warning("No python version installed. Please, install python")
            return None
        
    except FileNotFoundError:
        l.error("No Python interpreter found. Cannot create virtual environment.")
        return None

    except subprocess.CalledProcessError:
        l.error("Could not list Python versions with 'py -0'.")
        return None

def load_config(config_file):
    file_path = Path(__file__).resolve().parent/config_file
    
    with open(file_path, "r", encoding="utf-8") as file:
        scaffold = yaml.safe_load(file)

    return scaffold


def resolve_template(config, template_arg):
    template_path = Path(template_arg)

    if template_path.exists():
        
        l.info(f"Using custom template file: {template_path}")
        
        with open(template_path, "r", encoding="utf-8") as file:
            custom_config = yaml.safe_load(file)
        
        return custom_config.get("template")

    
    if template_arg in config["templates"]:

        l.info(f"Using built-in template: {template_arg}")

        return config["templates"][template_arg]

    l.error(f"Template '{template_arg}' not found.")
    return None



def parse_args():
    parser = argparse.ArgumentParser(
        prog="python-forge",
        description="Create Python project scaffolds quickly and consistently.",
        epilog="Example: python forge.py create my_project basic --python 3.12",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "command",
        choices=["create"],
        help="Action to perform (currently only 'create')."
    )

    parser.add_argument(
        "project_name",
        help= "Name of the project to create."
        )

    parser.add_argument(
        "template",
        help="Template name from projects.yaml or path to a custom YAML template."
    )
    
    default_python = get_default_py_version()

    parser.add_argument(
        "--python",
        default=default_python,
        metavar="VERSION",
        help="Python version to use for the virtual environment (e.g. 3.12)." 
    )

    parser.add_argument(
        "--no-git",
        action="store_true",
        help= "Skip Git initialization and first commit."
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help= "Apply template to an existing project without confirmation."
    )

    parser.add_argument(
        "--no-venv",
        action="store_true",
        help="Skip virtual environment creation.",
    )
    
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory where the project will be created. By default, it is created next to python-forge.",
    )




    return parser.parse_args()





def create_project(config, project_name, template_name, output_dir, force = False):

    template = resolve_template(config, template_name)
    if template is not None:
        l.info(f"Template description: {template.get('description', 'No description')}")
        structure = template["structure"]
        folders = structure["folders"]
        files = structure["files"]
    else:
        l.error("No scaffold project detected. Please, pass a valid YAML")
        return None

    ROOT_DIR = Path(__file__).resolve().parent
    PROJECTS_DIR = ROOT_DIR.parent

    if output_dir is None:
        target_dir = PROJECTS_DIR
    else:
        target_dir = Path(output_dir).expanduser().resolve()

    base_path = Path(target_dir / project_name)
    package_name = normalize_package_name(project_name)
    l.info(f"Creating project: {project_name}.")
    l.info(f"Package name: {package_name}")
    l.info(f"Target path: {base_path}")

    if base_path.exists():
        if force:
            l.info("Project exists → forcing update.")
        else:
            l.warning("-------- Project already exists! ----------- \n"
            "Do you want to update? (Y/n)")

            ans = input("> ").casefold()

            while ans not in ("y", "n"):
                l.info("Please answer 'y' or 'n'")
                ans = input("> ").casefold()
            
            if ans == "n":
                l.info("Ok! Check your projects and try again.")
                return None
            else:
                l.info("Project Updated!")
    
    else:
        base_path.mkdir(parents = True, exist_ok=True)
    
    l.info("Creating Folders:")
    for folder in folders:
        folder = render_template_text(folder, project_name)
        folder_path = Path(base_path / folder)
        if folder_path.exists():
            continue
        folder_path.mkdir(parents=True, exist_ok = True)

        print(f"          - {folder}")


    l.info("Creating Files:")
    for file, content in files.items():
        file = render_template_text(file, project_name)
        full_path = Path(base_path/file)

        if full_path.exists():
            continue
        
        if content is None:
            content = ""

        content = render_template_text(content, project_name)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")

        print(f"          - {file}")

    return base_path



def create_venv (python_version, env_path):
    venv_path = Path(env_path/".venv")
    if venv_path.exists():
        l.warning("-------- Virtual Environment already exists --------")
        return False
    
    l.info("Creating virtual environment...")
    try:
        subprocess.run(
            ["py", f"-{python_version}", "-m", "venv", ".venv"],
            cwd=env_path, check= True)
        l.info("Virtual environment created.")
        return True
    except subprocess.CalledProcessError as err:
        l.error("Failed to create virtual environment.")
        if err.stderr:
            print(err.stderr)
        return False



def init_commit_git(project_path):

    git_path = project_path/".git"

    if git_path.exists():
        l.warning("-------- Git repository already initialized --------")
        return False
    
    try:
        l.info("Check git installation")
        check_git = subprocess.run(
            ["git", "--version"],
            cwd= project_path,
            check=True, capture_output=True,
            text=True
        )
        if check_git.stdout:
            print(check_git.stdout)

        l.info("Initializing git repository...")

        subprocess.run(
            ["git", "init"],
            cwd= project_path,
            check=True
        )

        l.info("Git repository initialized.")

        try:
            result_name = subprocess.run(
                ["git", "config", "--global", "user.name"],
                check=True,
                text=True,
                capture_output=True
            )

            result_email = subprocess.run(
                ["git", "config", "--global", "user.email"],
                check=True,
                text=True,
                capture_output=True
            )
            git_name = result_name.stdout.strip()
            git_email = result_email.stdout.strip()

            if not git_name or not git_email:
                raise subprocess.CalledProcessError(1, "git config")

            l.info(f"Git credentials: {git_name} -> {git_email}")

            


        except subprocess.CalledProcessError as CPE:
            l.warning("Git credentials not configured.")

            git_name = input("Enter git user.name: ").strip()
            git_email = input("Enter git user.email: ").strip()
            
            subprocess.run(
                ["git", "config", "--global", "user.name", git_name],
                check=True
            )

            subprocess.run(
                ["git", "config", "--global", "user.email", git_email],
                check=True
            )



        l.info("Adding project structure to first commit...")
        subprocess.run(
            ["git", "add", "."],
            cwd=project_path, check= True
        )
        l.info("Project structure added!")
        l.info("Committing...")
        git_commit_return = subprocess.run(
            ["git", "commit", "-m", "Initial Commit"],
            cwd=project_path, 
            check=True, 
            capture_output=True,
            text=True
        )
        l.info("Initial commit created.")
        if git_commit_return.stdout:
            print(git_commit_return.stdout)
        
        return True

    except FileNotFoundError:
        l.error("Git is not installed or not available in PATH.")
        
        return False

    except subprocess.CalledProcessError as err:
        l.error("Git command failed")
        if err.stdout:
            print(err.stdout)
        if err.stderr:
            print(err.stderr)
        
        return False
        
def print_summary(project_path, args, venv_created, git_created):
    print("\n========== SUMMARY ==========")

    l.info(f"Project: {project_path.name}")
    l.info(f"Location: {project_path}")

    l.info(f"Template: {args.template}")

    if args.no_venv:
        l.info("Venv: skipped")
    else:
        l.info(f"Venv: {'created' if venv_created else 'Not created'} (Python {args.python})")

    if args.no_git:
        l.info("Git: skipped")
    else:
        l.info(f"Git: {'initialized' if git_created else 'Not initialized'}")
    
    print("=============================")




def main():

    args = parse_args()

    scaffold = load_config(CONFIG_FILE)

    project_path = create_project(scaffold,
                                    project_name=args.project_name,
                                    template_name=args.template,
                                    force=args.force,
                                    output_dir=args.output_dir)

    if project_path is None:
        return
    
    venv_created = False
    git_created = False

    if not args.no_venv:
        if args.python is None:
            l.error("No Python interpreter found. Cannot create virtual environment.")
            
            return

        venv_created = create_venv(python_version= args.python, env_path=project_path)
    
    if not args.no_git:
        git_created = init_commit_git(project_path)
    
    print_summary(project_path, args, venv_created, git_created)
    

if __name__== "__main__":
    main()
