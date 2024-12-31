from api.db.database import Base

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, ForeignKey, func


class ModelBase(Base):
    __abstract__ = True
    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


class User(ModelBase):
    __tablename__ = 'users'
    email = Column(String, unique=True, index=True, nullable=False)
    fullname = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Message(ModelBase):
    __tablename__ = 'messages'
    sender_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(UUID, ForeignKey('users.id'), nullable=False)
    message_text = Column(String, nullable=True)
    message_image = Column(String, nullable=True)
    