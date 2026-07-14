def build_prompt(repository_report, user_question):
    prompt = "Repository security Check\n\n"
    prompt += """ You are a repository security assistant.
Answer only from the repository scan report below.
Do not invent CVEs, versions, severity, or fixes.
If information is missing, say: Not available in this scan report.
Keep the answer short and in Markdown"""

    for report in repository_report:
        package = report["package"]
        vulnerabilities = report["vulnerabilities"]

        version = package["version"] or "unknown"

        prompt += f"package {package['name']}\n"
        prompt += f"Version {version}\n"

        if package["version"] is None:
            prompt += "⚠ Version not specified. OSV returned all known advisories. Some may not apply."

        if not vulnerabilities:
            prompt += "No known vulnerabilities.\n\n"
            continue

        prompt += f"Found {len(vulnerabilities)} vulnerabilities\n"

        for vuln in vulnerabilities[:3]:
            prompt += f"- {vuln['id']}\n"
            prompt += f"  Severity: {vuln['severity']}\n"

            summary = vuln['summary']
            if len(summary) > 200:
                summary = summary[:200] + "..."
            prompt += f"  Summary: {summary}\n\n"

        if len(vulnerabilities) > 3:
            prompt += f"...and {len(vulnerabilities)-3} more vulnerabilities.\n"

        prompt += "-" * 50 + "\n\n"

    prompt += f"User_question:{user_question}\n\n"

    return prompt