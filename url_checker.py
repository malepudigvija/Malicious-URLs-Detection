# url_checker.py
import re
import tldextract

# suspicious TLDs often used in phishing
SUSPICIOUS_TLDS = {"tk", "xyz", "top", "gq", "ml"}

# suspicious keywords often found in fake domains
SUSPICIOUS_KEYWORDS = [
    "login", "verify", "secure", "update", "account", "support",
    "banking", "webmail", "pay", "confirm"
]

# characters often used in look-alike domains
LOOKALIKE_PATTERNS = [
    ("0", "o"), ("1", "l"), ("rn", "m")  # simple examples
]

def check_url_heuristics(url: str):
    """Return (is_suspicious: bool, reasons: list)"""
    reasons = []
    ext = tldextract.extract(url)
    domain = ext.domain.lower()
    suffix = ext.suffix.lower()

    # 1. Check TLD
    if suffix in SUSPICIOUS_TLDS:
        reasons.append(f"Suspicious TLD: .{suffix}")

    # 2. Check suspicious keywords in domain or subdomain
    combined = f"{ext.subdomain}.{domain}"
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in combined:
            reasons.append(f"Contains suspicious keyword: {kw}")

    # 3. Check for look-alike patterns
    for a, b in LOOKALIKE_PATTERNS:
        if a in domain and b in domain:
            reasons.append(f"Look-alike pattern: both '{a}' and '{b}' in {domain}")
        # Or check if a suspicious char replaced another
        if a in domain:
            # Example: zero instead of o
            reasons.append(f"Possible look-alike: '{a}' in {domain}")

    # 4. Check overly long URL
    if len(url) > 100:
        reasons.append("URL is unusually long")

    # 5. Check encoded characters
    if "%" in url or "@" in url:
        reasons.append("URL contains encoded or special characters")

    is_suspicious = len(reasons) > 0
    return is_suspicious, reasons
