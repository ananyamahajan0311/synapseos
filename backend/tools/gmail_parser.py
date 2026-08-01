import re


def parse_email_command(command):
    result = {
        "to": "",
        "subject": "",
        "body": ""
    }

    # Recipient
    match = re.search(r"to\s+([^\s]+@[^\s]+)", command, re.IGNORECASE)
    if match:
        result["to"] = match.group(1)

    # Subject
    match = re.search(r"subject\s+(.*?)\s+body", command, re.IGNORECASE)
    if match:
        result["subject"] = match.group(1).strip()

    # Body
    match = re.search(r"body\s+(.*)", command, re.IGNORECASE)
    if match:
        result["body"] = match.group(1).strip()

    return result