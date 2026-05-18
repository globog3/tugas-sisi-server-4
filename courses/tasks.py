from celery import shared_task
import time


@shared_task
def send_enrollment_email(student_email):
    time.sleep(5)

    print(f"Email enrollment dikirim ke {student_email}")

    return f"Success send email to {student_email}"


@shared_task
def generate_certificate(student_name):
    time.sleep(5)

    print(f"Certificate dibuat untuk {student_name}")

    return f"Certificate generated for {student_name}"


@shared_task
def update_course_statistics():
    print("Update course statistics")

    return "Statistics updated"


@shared_task
def export_course_report():
    print("Generate CSV report")

    return "CSV report generated"