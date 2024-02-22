from backend.celery import app
from utils.emails import send_email
from organization.models import Organization
from celery.schedules import crontab

@app.task()
def send_number_plate_verification_email():
    organizations = Organization.objects.all()
    receivers = []
    for org in organizations:
        receivers.extend(org.admins)

    send_email(receiver="dgdeshmukh2002@gmail.com",subject= "ParkVision Admin Reminder",
    message=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ParkVision Admin Reminder</title>
    </head>
    <body style="font-family: Arial, sans-serif; text-align: center;">
        <div class="container" style="max-width: 600px; margin: 0 auto; background-color: #f4f2ee; padding: 25px; border-radius: 10px;">
            <h1 style="margin-top: 2.5rem; color: #8DBF41;">ParkVision Admin Reminder</h1>
            <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                Dear Admin, this is a reminder to log in and verify detected number plates on ParkVision.
            </p>
            <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                Ensure that all number plates are correctly identified and validated for accurate parking management.
            </p>
            <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                Thank you for your attention to this matter.
            </p>
            <p style="margin-top: 1.25rem; font-size: 16px; line-height: 1.5;">
                Best regards,
                <br>
                ParkVision Team
            </p>
        </div>
    </body>
    </html>
    """)

    print("The email has been sent!", flush= True)

