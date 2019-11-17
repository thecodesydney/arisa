from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content, Personalization, Email, Attachment,\
    FileContent, FileName, FileType, Disposition, ContentId
import base64

##############################################################################
# function you call to send an email using Sendgrid
##############################################################################


def send_email(subject, sender, recipients, text_body, html_body, file_path=None):
    # construct message
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject=subject,
        html_content=Content('text/html', html_body))
    txt_content = Content('text/txt', text_body)
    message.add_content(txt_content)

    # if there is an attachment add it
    if file_path is not None:
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                f.close()

            encoded = base64.b64encode(data).decode()
            # build attachment
            attachment = Attachment()
            attachment.file_content = FileContent(encoded)
            attachment.file_type = FileType('text/plain')
            attachment.file_name = FileName('report.txt')
            attachment.disposition = Disposition('attachment')
            attachment.content_id = ContentId('txt file')
            # add attachment to message
            message.attachment = attachment
        except IOError as e:
            print(e)
            return False

    try:
        sg = SendGridAPIClient(current_app.config['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return True
    except Exception as e:
        return False
