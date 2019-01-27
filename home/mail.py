from email.message import EmailMessage
import smtplib



def send_email(message,destination):
    # important, you need to send it to a server that knows how to send e-mails for you
    server = smtplib.SMTP('mima5us.havaso.com', 587)
    server.starttls()
    # don't know how to do it without cleartexting the password and not relying on some json file that you dont git control...
    server.login('wishlist@havaso.com', 'support_44_havaso')
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'TEST'
    msg['From'] = 'eyesonaleks@gmail.com'
    msg['To'] = destination
    server.send_message(msg)

message = "hello"

send_email(message, "eyesonaleks@gmail.com")


