import math
import os
from dataclasses import dataclass, field
from urllib.parse import quote, urlsplit, urlunsplit


@dataclass(frozen=True)
class Settings:
    base_url: str
    username: str = field(repr=False)
    password: str = field(repr=False)
    timeout: float = 15

    def __post_init__(self):
        parts = urlsplit(self.base_url)
        if parts.scheme != "https" or not parts.hostname:
            raise ValueError("ZAGS_BASE_URL must be an absolute HTTPS URL")
        if parts.username is not None or parts.password is not None:
            raise ValueError("Store credentials in ZAGS_USERNAME and ZAGS_PASSWORD, not in the URL")
        if parts.query or parts.fragment:
            raise ValueError("ZAGS_BASE_URL must not contain a query or fragment")
        if not self.username or not self.password:
            raise ValueError("Set ZAGS_USERNAME and ZAGS_PASSWORD in .env or environment")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ValueError("ZAGS_TIMEOUT must be a finite positive number")

    @classmethod
    def from_env(cls):
        return cls(
            base_url=os.getenv("ZAGS_BASE_URL", "https://regoffice.senla.eu/"),
            username=os.getenv("ZAGS_USERNAME", ""),
            password=os.getenv("ZAGS_PASSWORD", ""),
            timeout=float(os.getenv("ZAGS_TIMEOUT", "15")),
        )

    def authenticated_url(self):
        parts = urlsplit(self.base_url)
        credentials = f"{quote(self.username, safe='')}:{quote(self.password, safe='')}"
        return urlunsplit(parts._replace(netloc=f"{credentials}@{parts.netloc}"))
