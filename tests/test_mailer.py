import sys
from unittest.mock import Mock, ANY
sys.modules['boto3'] = Mock()
from src import mailer

def generate_no_interest_mail_body(name):
    with open('./emails/_header.txt', 'r') as f:
        header = f.read()
    with open('./emails/_footer.txt', 'r') as f:
        footer = f.read()
    content = header + "\n" +  footer
    content = content.replace('{%name%}', name)
    return content

def generate_interest_mail_body(name):
    with open('./emails/_header.txt', 'r') as f:
        header = f.read()
    with open('./emails/addons.txt', 'r') as f:
        addons = f.read()
    with open('./emails/issues.txt', 'r') as f:
        issues = f.read()
    with open('./emails/_footer.txt', 'r') as f:
        footer = f.read()
    content = header + "\n" + addons + "\n" + issues + "\n" + footer
    content = content.replace('{%name%}', name)
    return content

def test_send_email():
    # ses = MockBoto3()
    to_email = "foo@bar.com"
    from_email = "community@mozilla.org" # TODO:?
    cc_email = "cc@mozilla.org" # TODO:?
    subject = "Test Subject"
    name = "Foo Bar"

    body = "Hello Foo Bar"
    # content = generate_no_interest_mail_body(name)

    ses = Mock()
    mailer.send_email(ses, from_email, to_email, cc_email, subject, body)
    # ses.send_email.assert_called("foo")
    ses.send_email.assert_called_with(
        Destination = {'ToAddresses': [to_email], 'CcAddresses': [cc_email]},
        Message={'Subject': {'Data': subject},
                 'Body': {'Text': {'Data': body}}},
        Source=from_email)

def test_format_body():
    name = "Foo Bar"
    interests = []
    content = generate_no_interest_mail_body(name)

    assert mailer.format_body(name, interests) == content

def test_content_variables():
    for key, val in mailer.contents.items():
        assert type(key) is str
        assert type(val) is str
        assert len(key) > 0
        assert len(val) > 0

def test_format_body_with_interests():
    name = "Foo Bar"
    interests = ['addons', 'issues']
    content = generate_interest_mail_body(name)

    assert mailer.format_body(name, interests) == content

def test_lambda_handler():
    event = {
        'name': 'Foo bar',
        'email': 'foo@bar.com',
        'interests': []
    }
    mailer.ses = Mock()
    mailer.send_email = Mock()

    mailer.lambda_handler(event, {});

    mailer.send_email.assert_called_with(mailer.ses,
                                         'contribute@moztw.org',
                                         'foo@bar.com',
                                         'contribute@moztw.org',
                                         'Hello from Mozilla',
                                         ANY)
    # TODO: We haven't check the email body
