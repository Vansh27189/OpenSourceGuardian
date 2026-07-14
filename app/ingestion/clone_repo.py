from pathlib import Path
from git import Repo, GitCommandError

REPO_FOLDER = Path("repositories")


def clone_repo(repo_url) -> Path:
    REPO_FOLDER.mkdir(exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    destination = REPO_FOLDER / repo_name

    if destination.exists():
        print("Repo already exist")
        return destination

    print("cloning Repo")

    try:
        Repo.clone_from(repo_url, destination)
    except GitCommandError as e:
        raise RuntimeError(f"Failed to clone {repo_url}: {e}") from e

    print("Clone Complete")

    return destination
