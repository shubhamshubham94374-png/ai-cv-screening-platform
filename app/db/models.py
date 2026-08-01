from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Enum, Text, Float, UniqueConstraint, JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db.session import Base


class UploadStatus(str, enum.Enum):
    uploaded = "uploaded"
    parsing = "parsing"
    parsed = "parsed"
    failed = "failed"


class SkillSource(str, enum.Enum):
    listed = "listed"
    inferred = "inferred"


class RequirementType(str, enum.Enum):
    required = "required"
    preferred = "preferred"


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_hash = Column(String, nullable=False, index=True)
    file_size_kb = Column(Integer, nullable=False)
    upload_status = Column(Enum(UploadStatus), default=UploadStatus.uploaded, nullable=False)
    is_duplicate = Column(Boolean, default=False, nullable=False)
    duplicate_of_candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=True)

    name = Column(String, nullable=True)
    email = Column(String, nullable=True, index=True)
    phone = Column(String, nullable=True)
    linkedin = Column(String, nullable=True)
    github = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)

    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    skills = relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="candidate", cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="candidate", cascade="all, delete-orphan")
    certifications = relationship("Certification", back_populates="candidate", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="candidate", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    candidates = relationship("CandidateSkill", back_populates="skill")


class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    __table_args__ = (UniqueConstraint("candidate_id", "skill_id", name="uq_candidate_skill"),)

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    source = Column(Enum(SkillSource), default=SkillSource.listed, nullable=False)

    candidate = relationship("Candidate", back_populates="skills")
    skill = relationship("Skill", back_populates="candidates")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    institution = Column(String, nullable=True)
    degree = Column(String, nullable=True)
    field_of_study = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    gpa = Column(Float, nullable=True)

    candidate = relationship("Candidate", back_populates="education")


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    company = Column(String, nullable=True)
    role = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="experience")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    name = Column(String, nullable=False)
    issuer = Column(String, nullable=True)

    candidate = relationship("Candidate", back_populates="certifications")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="projects")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    raw_description = Column(Text, nullable=False)
    min_experience_years = Column(Integer, nullable=True)
    degree_requirement = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")


class JobSkill(Base):
    __tablename__ = "job_skills"
    __table_args__ = (UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),)

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    requirement_type = Column(Enum(RequirementType), nullable=False)

    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill")

class MatchScore(Base):
    __tablename__ = "match_scores"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    required_skills_score = Column(Float, nullable=False)
    preferred_skills_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    competencies_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    certifications_score = Column(Float, nullable=False)
    projects_score = Column(Float, nullable=False)
    domain_experience_score = Column(Float, nullable=False)

    total_score = Column(Float, nullable=False)

    missing_required_skills = Column(JSON, nullable=True)
    missing_preferred_skills = Column(JSON, nullable=True)

    computed_at = Column(DateTime(timezone=True), server_default=func.now())

    candidate = relationship("Candidate")
    job = relationship("Job")

class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    summary = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    interview_questions = Column(JSON, nullable=True)
    recommendation = Column(String, nullable=True)
    recommendation_justification = Column(Text, nullable=True)

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    candidate = relationship("Candidate")
    job = relationship("Job")