from typing import Optional
from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, DateTime, Boolean, text
from sqlalchemy.sql import func



class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    verified_email: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    sex: Mapped[Optional[str]] = mapped_column(nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=True)

    is_oauth: Mapped[bool] = mapped_column(default=False) 
    oauth_provider: Mapped[Optional[str]] = mapped_column(nullable=True)

    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

class MeasurementLog(Base):
    __tablename__ = "measurement_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight_kg: Mapped[float] = mapped_column(nullable=False)
    chest_cm: Mapped[float | None]
    waist_cm: Mapped[float | None]
    arm_cm: Mapped[float | None] 
    thigh_cm: Mapped[float | None] 

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))