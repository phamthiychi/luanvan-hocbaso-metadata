import os
import re
import sys
import json
import shutil
import asyncio
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# API
from src.adapter.database.mongo_manager import mongo_manager
from src.adapter.database.mongo_repository import (
    MongoAcademicYearRepository,
    MongoClassRepository,
    MongoGradeLevelRepository,
    MongoStudentRepository,
    MongoTeacherRepository,
    MongoSubjectRepository
)

SESSION = mongo_manager.get_core_db()
STUDENT_REPO = MongoStudentRepository(SESSION)
ACADEMIC_YEAR_REPO = MongoAcademicYearRepository(SESSION)
GRADE_LEVEL_REPO = MongoGradeLevelRepository(SESSION)
CLASS_ROOM_REPO = MongoClassRepository(SESSION)
TEACHER_REPO = MongoTeacherRepository(SESSION)
SUBJECT_REPO = MongoSubjectRepository(SESSION)

WORD2NUM = {
    "Một": 1,
    "Hai": 2,
    "Ba": 3,
    "Bốn": 4,
    "Năm": 5
}
WORD2SHORTCUT = {
    "Một": "Mo",
    "Hai": "Ha",
    "Ba": "Ba",
    "Bốn": "Bo",
    "Năm": "Na"
}
SUBJECT2SHORTCUT = {
    "Tiểu học": "TH",
    "Âm nhạc": "AN",
    "Thể dục": "TD",
    "Tin học": "TiH",
    "Tiếng Anh": "TA"
}
SHORTCUT2WORD = {v: k for k, v in WORD2SHORTCUT.items()}
NUM2WORD = {v: k for k, v in WORD2NUM.items()}

def extract(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def create_academic_year_code(academic_year) -> str:
    return f'NH{academic_year.replace(" - ", "")}'

def create_grade_level_code(class_room) -> str:
    return f"MK{WORD2NUM[class_room.split(' ')[0]]:02}"

def create_class_code(class_room, grade_level_code) -> str:
    result = class_room.split(" ")
    return f"{grade_level_code[-3:]}.ML{WORD2SHORTCUT[result[0]]}{result[1]}"

def create_student_code(index, academic_year_code, grade_level_code, class_code) -> str:
    return f"{academic_year_code[2:]}.{grade_level_code[-2:]}.{class_code[-3:]}.{index:03}"

def create_teacher_code(index, subject) -> str:
    return f'{SUBJECT2SHORTCUT[subject]}.GV{index:02}'

def get_data_base_on_profile_type(row, profile_type) -> dict:
    if profile_type == "student":
        return {
            "name": row.get("Họ tên"),
            "date_of_birth": pd.to_datetime(row.get("Ngày sinh"),
                                            errors="coerce") \
                             .strftime("%Y-%m-%d"),
            "gender": row.get("Giới tính"),
            "ethnicity": row.get("Dân tộc"),
            "nationality": row.get("Quốc tịch"),
            "card_id": str(row.get("Số CCCD")),
            "edu_id": str(row.get("Mã định danh Bộ GD&ĐT")),
            "status": row.get("Trạng thái HS"),
            "phone": f'0{str(row.get("Số điện thoại liên hệ"))}',
            "address": row.get("Chỗ ở hiện nay chi tiết"),
            "class_room": row.get("Mã lớp")
        }
    elif profile_type == "teacher":
        if row.get("Vị trí việc làm") != "Giáo viên":
            return None
        return {
            "name": row.get("Họ tên"),
            "date_of_birth": pd.to_datetime(row.get("Ngày sinh"),
                                            errors="coerce") \
                             .strftime("%Y-%m-%d"),
            "gender": row.get("Giới tính"),
            "ethnicity": row.get("Dân tộc"),
            "nationality": "Việt Nam",
            "card_id": str(row.get("Số CMTND/TCC")),
            "edu_id": str(row.get("Mã định danh Bộ GD&ĐT")),
            "status": row.get("Trạng thái CB"),
            "phone": f'0{str(row.get("Điện thoại"))}',
            "specialization": row.get("Chuyên ngành chính"),
            "position": None if pd.isna(row.get("Nhóm chức vụ")) else row.get("Nhóm chức vụ"),
            "subject": row.get("Môn dạy")
        }

def preprocessing(file_xls, profile_type) -> list:
    df = pd.read_excel(file_xls)
    result = []
    for _, row in df.iterrows():
        data = get_data_base_on_profile_type(row, profile_type)
        if data:
            result.append(data)
    # if len(result) > 1:
    #     print(result)
    return result

async def create_and_update_teacher(teacher_code, info) -> None:
    teacher_repo = {
        "code": teacher_code,
        "name": info.get("name"),
        "date_of_birth":info.get("date_of_birth"),
        "gender": info.get("gender"),
        "ethnicity": info.get("ethnicity"),
        "nationality": info.get("nationality"),
        "card_id": info.get("card_id"),
        "edu_id": info.get("edu_id"),
        "status": info.get("status"),
        "phone": info.get("phone"),
        "specialization": info.get("specialization"),
        "position": info.get("position")
    }
    try:
        result = await TEACHER_REPO.add(teacher_repo)
        if result is None:
            try:
                await TEACHER_REPO.update(teacher_repo)
            except Exception:
                return None
        else:
            return teacher_repo
    except Exception as e:
        print(f"Error {e}")
        return None

async def create_and_update_student(student_code, info) -> None:
    student_record = {
        "code": student_code,
        "name": info.get("name"),
        "date_of_birth":info.get("date_of_birth"),
        "gender": info.get("gender"),
        "ethnicity": info.get("ethnicity"),
        "nationality": info.get("nationality"),
        "card_id": info.get("card_id"),
        "edu_id": info.get("edu_id"),
        "status": info.get("status"),
        "phone": info.get("phone"),
        "address": info.get("address"),
    }
    try:
        result = await STUDENT_REPO.add(student_record)
        if result is None:
            try:
                await STUDENT_REPO.update(student_record)
            except Exception:
                return None
        else:
            return student_record
    except Exception as e:
        print(f"Error {e}")
        return None

async def create_and_update_academic_year(academic_year_codes, start_date, end_date) -> None:
    for code in academic_year_codes:
        info = code[2:]
        mark = int(len(info) / 2)
        academic_year_record = {
            "code": code,
            "name": f"{info[:mark]}-{info[mark:]}",
            "start_date": start_date,
            "end_date": end_date,
        }
        result = await ACADEMIC_YEAR_REPO.add(academic_year_record)
        if result is None:
            await ACADEMIC_YEAR_REPO.update(academic_year_record)

async def create_and_update_grade_level(grade_level_codes) -> None:
    for code in grade_level_codes:
        max_students = 0
        class_rooms = list(SESSION["classes"].find({"code": {"$regex": f"^{code[-3:]}"}}))
        max_students += sum(cr.get("data").get("size") for cr in class_rooms)
        grade_level_record = {
            "code": code,
            "name": f"Khối {int(code.split('MK')[1])}",
            "max_students": max_students
        }
        result = await GRADE_LEVEL_REPO.add(grade_level_record)
        if result is None:
            await GRADE_LEVEL_REPO.update(grade_level_record)

async def create_and_update_class_room(class_room_codes, special_program, academic_year) -> None:
    for code in class_room_codes:
        students = list(SESSION["students"].find({"code": {"$regex": code[-3:]}}))
        class_room_record = {
            "code": code,
            "name": f'{SHORTCUT2WORD[code.split("ML")[1][:2]]} {code.split("ML")[1][2]}',
            "size": len(students),
            "grade_level_id": create_grade_level_code(f'{SHORTCUT2WORD[code.split("ML")[1][:2]]} {code.split("ML")[1][2]}'),
            "academic_year_id": create_academic_year_code(academic_year),
            "special_program": special_program
        }
        result = await CLASS_ROOM_REPO.add(class_room_record)
        if result is None:
            await CLASS_ROOM_REPO.update(class_room_record)

async def create_and_update_subject(subjects, total_periods_default = 30) -> None:
    for sub in subjects:
        subject_repo = {
            "code": f'MH{SUBJECT2SHORTCUT[sub]}',
            "name": sub,
            "total_periods": total_periods_default
        }
        result = await SUBJECT_REPO.add(subject_repo)
        if result is None:
            await SUBJECT_REPO.update(subject_repo)

async def import_data_from_student_profile(student_profile,
                                           requirement_info) -> None:
    info_from_student_profile = preprocessing(student_profile, "student")
    index = 1
    student_errors = []
    class_codes = set()
    grade_codes = set()
    academic_codes = set()
    for info in info_from_student_profile:
        academic_code = create_academic_year_code(f'{requirement_info["academic_year_start"].split("-")[0]} - '\
                                                  f'{requirement_info["academic_year_end"].split("-")[0]}')
        grade_code = create_grade_level_code(info.get("class_room"))
        class_code = create_class_code(info.get("class_room"), grade_code)
        if class_code not in class_codes:
            index = 1
        else:
            index = index + 1
        student_code = create_student_code(index,
                                           academic_code, grade_code, class_code)
        result = await create_and_update_student(student_code, info)
        if result is None:
            student_errors.append(info)
        academic_codes.add(academic_code)
        grade_codes.add(grade_code)
        class_codes.add(class_code)

    await create_and_update_class_room(list(class_codes), None, list(academic_codes)[0])
    await create_and_update_grade_level(list(grade_codes))
    await create_and_update_academic_year(list(academic_codes),
                                          requirement_info.get("academic_year_start"),
                                          requirement_info.get("academic_year_end"))
    if student_errors:
        with open("student_profile_error_mongo.json", "w", encoding="utf-8") as f:
            json.dump(student_errors, f, indent=4, ensure_ascii=False)

async def import_data_from_teacher_profile(teacher_profile) -> None:
    info_from_teacher_profile = preprocessing(teacher_profile, "teacher")
    index = 1
    teacher_error = []
    subjects = set()
    for info in info_from_teacher_profile:
        teacher_code = create_teacher_code(index, info.get("subject"))
        subjects.add(info.get("subject"))
        result = await create_and_update_teacher(teacher_code, info)
        if result is None:
            teacher_error.append(info)
        index = index + 1
    await create_and_update_subject(subjects)
    if teacher_error:
        with open("teacher_profile_error_mongo.json", "w", encoding="utf-8") as f:
            json.dump(teacher_error, f, indent=4, ensure_ascii=False)