"""Send a small JUnit report and a link; do not email personal test data."""

import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from xml.etree import ElementTree


def build_message(report, run_url):
    root = ElementTree.parse(report).getroot()
    cases = root.findall(".//testcase")
    failed = sum(c.find("failure") is not None for c in cases)
    errors = sum(c.find("error") is not None for c in cases)
    skipped = sum(c.find("skipped") is not None for c in cases)
    message = EmailMessage()
    message["Subject"] = f"ZAGS: {len(cases)} tests, {failed} failures, {errors} errors"
    message["From"] = os.environ.get("MAIL_FROM", "training@example.invalid")
    message["To"] = os.environ.get("MAIL_TO", "mentor@example.invalid")
    message.set_content(
        f"Tests: {len(cases)}; failures: {failed}; errors: {errors}; "
        f"skipped: {skipped}\nAllure artifact and logs: {run_url}\n"
    )
    message.add_attachment(
        Path(report).read_bytes(), maintype="application", subtype="xml", filename="junit.xml"
    )
    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--run-url", default="Local rehearsal; no CI run")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    message = build_message(args.report, args.run_url)
    if args.dry_run:
        print(message["Subject"])
        print("Dry run: message built; nothing sent")
        return
    required = ["SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "MAIL_FROM", "MAIL_TO"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError("Set SMTP configuration: " + ", ".join(missing))
    with smtplib.SMTP(
        os.environ["SMTP_HOST"], int(os.getenv("SMTP_PORT", "587")), timeout=20
    ) as smtp:
        smtp.starttls(context=ssl.create_default_context())
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(message)


if __name__ == "__main__":
    main()
