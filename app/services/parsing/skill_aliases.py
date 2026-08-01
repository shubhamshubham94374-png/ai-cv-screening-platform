SKILL_ALIASES = {
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "reactjs": "React",
    "react.js": "React",
    "nodejs": "Node.js",
    "node": "Node.js",
    "py": "Python",
    "ml": "Machine Learning",
    "k8s": "Kubernetes",
}


def normalize_skill_name(skill_name: str) -> str:
    """Returns the canonical skill name if a known alias exists, otherwise returns the input unchanged."""
    return SKILL_ALIASES.get(skill_name.strip().lower(), skill_name)