from anymail.message import AnymailMessage


def send_email(
        *,
        subject: str,
        body: str,
        to: list,
        from_email: str = None,
        headers: dict = None,
):
    msg = AnymailMessage(
        subject=subject,
        body=body,
        to=to,
        from_email=from_email,
        headers=headers
    )
    msg.send()
    return msg.anymail_status.message_id
