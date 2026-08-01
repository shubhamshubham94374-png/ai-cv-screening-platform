import re

def extract_email(text: str) -> str | None:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None

def extract_phone(text: str) -> str | None:
    match = re.search(r"(\+?\d{1,3}[-.\s]?)?\d{10}", text)
    return match.group(0) if match else None

def _extract_link(text: str, domain_pattern: str) -> str | None:
    match = re.search(domain_pattern, text)
    if not match:
        return None

    end = match.end()
    # Check if immediately followed by markdown-style "](https://...)"
    paren_match = re.match(r"\]\((https?://[^\s)]+)\)", text[end:end + 300])
    if paren_match:
        return paren_match.group(1)

    url = match.group(0)
    if not url.startswith("http"):
        url = "https://" + url
    return url

def extract_linkedin(text: str) -> str | None:
    return _extract_link(text, r"(https?://)?(www\.)?linkedin\.com/in/[A-Za-z0-9\-_/]+")

def extract_github(text: str) -> str | None:
    return _extract_link(text, r"(https?://)?(www\.)?github\.com/[A-Za-z0-9\-_/]+")

def extract_portfolio_links(text: str) -> list[str]:
    all_urls = re.findall(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9\-]+\.[a-z]{2,}(?:/[^\s]*)?", text)
    excluded_domains = ["linkedin.com", "github.com", "gmail.com", "yahoo.com", "outlook.com"]
    return [url for url in all_urls if not any(domain in url for domain in excluded_domains)]