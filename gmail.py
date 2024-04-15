from base64 import urlsafe_b64decode
from datetime import datetime
from os import path
from typing import List

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

credentials = None

if path.exists("token.json"):
    credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
if not credentials or not credentials.valid:
    app_flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    credentials = app_flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(credentials.to_json())

service = build("gmail", "v1", credentials=credentials)


def get_label_id(label) -> tuple[str | None, HttpError | None]:
    try:
        req = service.users().labels().list(userId="me").execute()
        labels = list(
            map(lambda l: {"id": l["id"], "name": l["name"]}, req.get("labels", []))
        )
        label_id = None
        for _label in labels:
            if _label["name"] == label:
                label_id = _label["id"]
        return (label_id, None)
    except HttpError as error:
        return (None, error)


def create_label(
    label, txt_color="#ffffff", bg_color="#fb4c2f"
) -> tuple[str | None, HttpError | None]:
    try:
        req = (
            service.users()
            .labels()
            .create(
                userId="me",
                body={
                    "name": label,
                    "messageListVisibility": "show",
                    "labelListVisibility": "labelShowIfUnread",
                    "color": {"textColor": txt_color, "backgroundColor": bg_color},
                },
            )
            .execute()
        )
        return (req.get("id"), None)
    except HttpError as error:
        return (None, error)


def apply_label(label_id, email_ids) -> HttpError | None:
    try:
        service.users().messages().batchModify(
            userId="me", body={"ids": email_ids, "addLabelIds": [label_id]}
        ).execute()
        return None
    except HttpError as error:
        return error


def recent_mail(max=10) -> tuple[list[dict[str, str]], HttpError | None]:
    try:
        req = (
            service.users()
            .messages()
            .list(userId="me", maxResults=max, q="is:unread is:important")
            .execute()
        )
        msgs = req.get("messages")
        if not msgs:
            return ([], None)

        recent_msgs = []
        for msg in msgs:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg.get("id"), format="raw")
                .execute()
            )
            msg = {
                "id": msg.get("id"),
                "labelIds": msg.get("labelIds"),
                "snippet": msg.get("snippet", "").strip(),
                "date": _date_from_epoch(msg.get("internalDate", 0)),
                "sizeEstimate": msg.get("sizeEstimate"),
                "text": _parse_mail(msg.get("raw", "")),
            }
            recent_msgs.append(msg)
        return (recent_msgs, None)
    except HttpError as error:
        return ([], error)


def _date_from_epoch(epochms):
    MILLISECONDS_IN_SECOND = 1000

    date = datetime.utcfromtimestamp(int(epochms) / MILLISECONDS_IN_SECOND)
    date = f"{date.month:02}/{date.day:02}/{date.year:02} @ {date.hour:02}:{date.minute:02}:{date.second:02}"
    return date


def _parse_mail(body):
    htmldoc = urlsafe_b64decode(body).decode()
    soup = BeautifulSoup(htmldoc, "html.parser")
    paragraphs = soup.find_all("p")
    results = ""
    for p in paragraphs:
        results += p.text.strip() + "\n"
    return results
