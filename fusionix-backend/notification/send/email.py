from email.message import EmailMessage
import smtplib , os, json

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]
        msg = EmailMessage()
        msg.set_content(f"Mp3 file id: {mp3_fid} is now ready to download")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address
        session = smtplib.SMTP("smtp.gmail.com",587)
        session.starttls()
        session.login(sender_address,sender_password)
        session.send_message(msg,sender_address,receiver_address)
        session.quit()
        print(f"Mail with mp3_fid: {mp3_fid} has successfully sent")
    except Exception as err:
        print(f"Notification Error:{err}")
        return "internal server error",500


