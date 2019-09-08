from send_to_kindle.sender.email_sender import EmailSender
from unittest.mock import patch, mock_open, MagicMock, call
from email.mime.multipart import MIMEBase, MIMEMultipart
from pathlib import Path
import pytest


def test_prepare_attachment(attachment_path):
    sender = EmailSender(None, None, None, 0, True)
    data = b"Some data"
    with patch("builtins.open", mock_open(read_data=data)):
        with patch(
            "send_to_kindle.sender.email_sender.MIMEBase", spec=MIMEBase
        ) as attachment_mock:
            with patch(
                "send_to_kindle.sender.email_sender.encode_base64"
            ) as encode_base64:
                attachment_mocked = attachment_mock.return_value
                sender.prepare_attachment(attachment_path)
                attachment_mocked.set_payload.assert_called_once_with(data)
                encode_base64.assert_called_once_with(attachment_mocked)


def test_prepare_message(from_email, subject, to_email):
    sender = EmailSender(from_email, None, None, 0, True)

    calls = [call("Subject", subject), call("To", [to_email]), call("From", from_email)]
    with patch("send_to_kindle.sender.email_sender.MIMEMultipart", spec=MIMEMultipart):
        message = sender.prepare_message(subject, [to_email])
        message.__setitem__.assert_has_calls(calls)


@patch("send_to_kindle.sender.email_sender.EmailSender.prepare_message")
@patch("send_to_kindle.sender.email_sender.EmailSender.prepare_attachment")
@patch("send_to_kindle.sender.email_sender.smtplib.SMTP")
@pytest.mark.parametrize(["use_tls"], [([True]), ([False])])
def test_send_mail(
    smtp_mock,
    prepare_attachment_mock,
    prepare_message_mock,
    from_email,
    password,
    host,
    port,
    subject,
    to_email,
    attachment_path,
    use_tls,
):
    message = MagicMock()
    message_str = "Message"
    message.as_string.return_value = message_str
    attachment = MagicMock()

    sender = EmailSender(from_email, password, host, port, use_tls)

    smtp = MagicMock()
    smtp_mock.return_value.__enter__.return_value = smtp
    prepare_message_mock.return_value = message
    prepare_attachment_mock.return_value = attachment

    sender.send_mail(subject, to_email, attachment_path)

    message.attach.assert_called_once_with(attachment)
    smtp.login.assert_called_once_with(from_email, password)
    if use_tls:
        smtp.starttls.assert_called_once()
    else:
        smtp.starttls.assert_not_called()
    smtp.sendmail.assert_called_once_with(from_email, [to_email], message_str)


@pytest.mark.parametrize(
    ["addresses", "expected"],
    [
        ("a@mail.com,f@mail.com", ["a@mail.com", "f@mail.com"]),
        ("a@gmail.com, aaa@bb.com", ["a@gmail.com", "aaa@bb.com"]),
    ],
)
def test_get_addresses(addresses, expected, from_email):
    sender = EmailSender(from_email, None, None, 0, True)
    actual = sender.get_addresses(addresses)
    assert actual == expected
