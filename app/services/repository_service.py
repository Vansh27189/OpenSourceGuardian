from app.ingestion.clone_repo import clone_repo
from app.ingestion.detect_language import detect_language
from app.ingestion.dependency_file_finder import find_dependency
from app.ingestion.parser import parse_dependency_file
from app.vulnerability.osv_client import query_osv_batch, simplify_vulnerabilities


def analyse_repo(url_path):
    repo = clone_repo(url_path)

    language = detect_language(repo)
    print(f"Language: {language}")

    files = find_dependency(repo)
    print(f"Dependency files found: {files}")

    repository_report = []
    all_packages = []

    for file in files:
        packages = parse_dependency_file(file)
        print(f"Packages from {file}: {packages}")
        all_packages.extend(packages)

    print(f"Total packages found: {len(all_packages)}")

    if not all_packages:
        print("No packages found in supported dependency files.")
        return {
            "repository": url_path,
            "language": language,
            "report": [],
        }

    for package in all_packages:
        print(f"checking {package['name']}")

    try:
        batch_result = query_osv_batch(all_packages)
    except Exception as e:
        print(f"Batch OSV query failed: {e}")
        batch_result = {"results": [{} for _ in all_packages]}

    for package, result in zip(all_packages, batch_result.get("results", [])):
        vulnerabilities = simplify_vulnerabilities(result)

        repository_report.append(
            {
                "package": package,
                "vulnerabilities": vulnerabilities,
            }
        )

    print("\nRepository scan complete!")

    return {
        "repository": url_path,
        "language": language,
        "report": repository_report,
    }