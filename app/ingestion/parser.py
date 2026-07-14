from pathlib import Path
import tomllib
import json

def parse_dependency_string(dependency: str):
    dependency = dependency.strip()
    dependency = dependency.split("#", maxsplit=1)[0].strip()

    if not dependency:
        return None

    operators = ["==", ">=", "<=", "~=", "!=", ">", "<"]

    for operator in operators:
        if operator in dependency:
            name, version = dependency.split(operator, maxsplit=1)
            return {
                "name": name.strip(),
                "version": version.strip(),
                "ecosystem": "python",
            }

    return {
        "name": dependency,
        "version": None,
        "ecosystem": "python",
    }


def parse_python_requirements(file_path: Path):
    packages = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-16") as file:
            lines = file.readlines()

    for line in lines:
        package = parse_dependency_string(line)
        if package:
            packages.append(package)

    return packages


def parse_toml(file_path: Path):
    packages = []
    with open(file_path, "rb") as file:
        data = tomllib.load(file)

    dependencies = data.get("project", {}).get("dependencies", [])

    for dependency in dependencies:
        package = parse_dependency_string(dependency)
        if package:
            packages.append(package)
    return packages


def parse_json(file_path: Path):
    packages = []

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    dependencies = data.get("dependencies", {})

    for name, version in dependencies.items():
        package = {
            "name": name,
            "version": version,
            "ecosystem": "npm"
        }
        packages.append(package)

    return packages


def parse_dependency_file(file_path: Path):
    if file_path.name == "requirements.txt":
        return parse_python_requirements(file_path)

    if file_path.name == "pyproject.toml":
        return parse_toml(file_path)

    if file_path.name == "package.json":
        return parse_json(file_path)

    return []