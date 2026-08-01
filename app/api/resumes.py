from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Candidate, UploadStatus
from app.services.validation import validate_file, compute_file_hash
from app.services.storage.local_storage import LocalStorage
from app.services.parsing.resume_parser import parse_resume
from app.services.skill_service import link_skills_to_candidate
from app.core.config import settings

router = APIRouter(prefix="/resumes", tags=["Resumes"])
from app.services.storage.s3_storage import S3Storage

if settings.storage_backend == "s3":
    storage = S3Storage(bucket_name=settings.s3_bucket_name, region=settings.aws_region)
else:
    storage = LocalStorage(settings.upload_dir)


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_bytes = await file.read()

    validate_file(file.filename, file_bytes)
    file_hash = compute_file_hash(file_bytes)

    existing = db.query(Candidate).filter(Candidate.file_hash == file_hash).first()

    file_path = storage.save(file_bytes, file.filename)

    candidate = Candidate(
        original_filename=file.filename,
        file_path=file_path,
        file_hash=file_hash,
        file_size_kb=len(file_bytes) // 1024,
        is_duplicate=bool(existing),
        duplicate_of_candidate_id=existing.id if existing else None,
        upload_status=UploadStatus.parsing,
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    try:
        parsed = parse_resume(file_path)
        candidate.name = parsed["name"]
        candidate.email = parsed["email"]
        candidate.phone = parsed["phone"]
        candidate.linkedin = parsed["linkedin"]
        candidate.github = parsed["github"]
        candidate.raw_text = parsed["raw_text"]
        candidate.upload_status = UploadStatus.parsed

        link_skills_to_candidate(db, candidate.id, parsed["skills"])

    except Exception as e:
        import traceback
        print(f"PARSING ERROR: {e}")
        traceback.print_exc()
        candidate.upload_status = UploadStatus.failed

    db.commit()
    db.refresh(candidate)

    return {
        "candidate_id": candidate.id,
        "filename": candidate.original_filename,
        "status": candidate.upload_status,
        "is_duplicate": candidate.is_duplicate,
        "duplicate_of_candidate_id": candidate.duplicate_of_candidate_id,
        "name": candidate.name,
        "email": candidate.email,
        "skills": [cs.skill.name for cs in candidate.skills],
    }