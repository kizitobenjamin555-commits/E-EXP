from celery import shared_task
import csv
import io
from django.utils import timezone
from django.db import transaction
from .models import CSVUpload, School, ClassRoom, Student, Subject, Parent
from .utils import parse_subjects_field, generate_student_id_and_seq, create_user_for_student, DEFAULT_SCHOOL_CODE

@shared_task(bind=True)
def process_csv_upload(self, upload_id):
    try:
        upload = CSVUpload.objects.get(id=upload_id)
    except CSVUpload.DoesNotExist:
        return {'error': 'upload not found'}

    upload.status = 'processing'
    upload.save()

    created = 0
    updated = 0
    errors = []

    file_field = upload.file
    try:
        file_field.open(mode='rb')
        raw = file_field.read()
        text = raw.decode('utf-8')
        reader = csv.DictReader(io.StringIO(text))
        for idx, row in enumerate(reader, start=1):
            try:
                first_name = row.get('first_name', '').strip()
                last_name = row.get('last_name', '').strip()
                dob = row.get('dob', '').strip()
                gender = row.get('gender', '').strip()
                class_code = row.get('class_code', '').strip() or 'UNKNOWN'
                admission_year = int(row.get('admission_year') or 0)
                parent1_name = row.get('parent1_name', '').strip()
                parent1_email = row.get('parent1_email', '').strip()
                parent1_phone = row.get('parent1_phone', '').strip()
                subjects_field = row.get('subjects', '')

                # generate student id
                student_id = generate_student_id_and_seq(DEFAULT_SCHOOL_CODE, class_code, admission_year)

                # ensure classroom exists
                school = School.objects.filter(code=DEFAULT_SCHOOL_CODE).first()
                classroom, _ = ClassRoom.objects.get_or_create(school=school, code=class_code, year=admission_year, defaults={'name': f"{class_code} - {admission_year}"})

                # create user and student record
                user = create_user_for_student(first_name, last_name, student_id)
                student = Student.objects.create(
                    id=student_id,
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    classroom=classroom,
                    admission_year=admission_year,
                    gender=gender or None,
                )

                # create parent record if present
                if parent1_name:
                    Parent.objects.create(name=parent1_name, email=parent1_email or None, phone=parent1_phone or None)

                # subjects - ensure subject objects exist (no assignment here)
                subjects = parse_subjects_field(subjects_field)
                for code in subjects:
                    Subject.objects.get_or_create(code=code, defaults={'name': code})

                created += 1
            except Exception as e:
                errors.append({'row': idx, 'error': str(e)})

        upload.status = 'completed'
        upload.processed_at = timezone.now()
        upload.created_count = created
        upload.updated_count = updated
        upload.errors = errors or None
        upload.save()
        return {'created': created, 'updated': updated, 'errors': errors}
    except Exception as e:
        upload.status = 'error'
        upload.errors = {'exception': str(e)}
        upload.save()
        return {'error': str(e)}
