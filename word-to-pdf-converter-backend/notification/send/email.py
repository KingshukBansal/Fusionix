from email.message import EmailMessage
import smtplib, os, json

def notification(message):
    try:
        message = json.loads(message)
        docx_fid = message["docx_fid"]
        sender_address = os.environ.get("GMAIL_ADDRESS")
        sender_password = os.environ.get("GMAIL_PASSWORD")
        receiver_address = message["username"]

        # URL for the PDF file download (You need to replace this with the actual URL for the PDF)
        download_url = f"{os.environ.get('BASE_URL')}/download?fid={docx_fid}"

        # Creating an HTML email with a download button
        email_content = f"""
        <html>
        <body>
            <p>Dear User,</p>
            <p>Your PDF file with ID <b>{docx_fid}</b> is ready for download.</p>
            <a href="{download_url}" style="
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            ">Download PDF</a>
            <p>Thank you for using our service!</p>
        </body>
        </html>
        """

        # Create the email message
        msg = EmailMessage()
        msg.set_content(email_content, subtype="html")  # Specify the content type as HTML
        msg["Subject"] = "PDF Download Ready"
        msg["From"] = sender_address
        msg["To"] = receiver_address

        # Send the email
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg)
        session.quit()
        print(f"Mail with pdf_fid: {docx_fid} has been successfully sent")
        
    except Exception as err:
        print(f"Notification Error: {err}")
        return "internal server error", 500
