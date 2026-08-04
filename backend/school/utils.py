from __future__ import annotations
import secrets

from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .models import StudentSequence, Student, School

User = get_user_model()

DEFAULT_SCHOOL_CODE = 'EEXP'


def parse_subjects_field(s):
    if not s:
        return []
    return [c.strip().upper() for c in s.split(';') if c.strip()]


def normalize_username(first_name, last_name, student_id=None):
    base = f"{first_name} {last_name}".strip().upper()
    username = base
    if User.objects.filter(username=username).exists():
        if student_id:
            # append the sequence portion of the student_id to guarantee uniqueness
            seq_part = student_id.split('-')[-1]
            username = f"{base}-{seq_part}"
        else:
            # append random suffix
            username = f"{base}-{secrets.token_hex(3)}"
    return username


@transaction.atomic
def generate_student_id_and_seq(school_code, class_code, year):
    school = School.objects.filter(code=school_code).first()
    if not school:
        # create minimal school record
        school = School.objects.create(code=school_code, name=school_code)
    seq_obj, created = StudentSequence.objects.select_for_update().get_or_create(
        school=school, class_code=class_code, year=year,
        defaults={'last_seq': 0}
    )
    seq_obj.last_seq += 1
    seq_obj.save()
    next_seq = seq_obj.last_seq
    student_id = f"{school.code}-{class_code}-{year}-{next_seq:04d}"
    return student_id


def create_user_for_student(first_name, last_name, student_id):
    """
    Create a User for a student where the password is the student's StudentID.
    NOTE: Per your selection, the StudentID will act as the account password.
    The password is hashed before storage; the plaintext StudentID is not stored separately
    (it can be derived from the Student record).

    Returns the created User instance.
    """
    username = normalize_username(first_name, last_name, student_id)
    # Use the StudentID itself as the password (hashed in DB)
    password_hash = make_password(student_id)
    user = User.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password_hash,
        must_change_password=False,
        role='student',
    )
    return user
