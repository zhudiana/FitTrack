from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey



class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    sex: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
   

class MeasurementLog(Base):
    __tablename__ = "measurement_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    weight_kg: Mapped[float] = mapped_column(nullable=False)
    chest_cm: Mapped[float | None]
    waist_cm: Mapped[float | None]
    arm_cm: Mapped[float | None] 
    thigh_cm: Mapped[float | None] 

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))