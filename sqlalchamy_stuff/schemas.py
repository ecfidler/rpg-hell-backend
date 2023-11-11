from sqlalchemy import (
    Boolean, Column, Date, DateTime, ForeignKey, Integer, String
)
from sqlalchemy.orm import relationship

from .database import Base


class Objects(Base):
    # id, name, effect, times_selected
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    effect = Column(String, nullable=False)
    times_selected = Column(Integer, nullable=False, default=0)
    
    items = relationship(
        "Items", primaryjoin="Mention.msg_id == Message.id"
    )
    attachments = relationship("Attachment")
    


class Items(Base):
    # id, cost, craft
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False)
    msg_id = Column(String, ForeignKey("message.id"), nullable=False)
    mention = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Traits(Base):
    # id, dice, is_passive
    __tablename__ = "traits"

    id = Column(Integer, primary_key=True, nullable=False)
    msg_id = Column(String, ForeignKey("message.id"), nullable=False)
    url = Column(String, nullable=False)
    sticker = Column(Boolean, nullable=False, default=False)


class (Base):
    __tablename__ = "reaction"

    msg_id = Column(
        String, ForeignKey("message.id"), primary_key=True, nullable=False
    )
    member_id = Column(
        String, ForeignKey("member.id"), primary_key=True, nullable=False
    )
    emoji = Column(String, primary_key=True, nullable=False)
    timestamp = Column(DateTime)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(String, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String)
    thread = Column(Boolean, default=False, nullable=False)
    type = Column(String, nullable=False)

    messages = relationship("Message")


class VoiceEvent(Base):
    __tablename__ = "voice_event"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    member_id = Column(String, ForeignKey("member.id"), nullable=False)
    type = Column(String, nullable=False)
    channel = Column(String, ForeignKey("channel.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)


class Score(Base):
    __tablename__ = "score"

    epoch = Column(Integer, primary_key=True, index=True, nullable=False)
    member_id = Column(
        String, ForeignKey("member.id"), primary_key=True, nullable=False
    )
    score = Column(Integer, nullable=False)


class Member(Base):
    __tablename__ = "member"

    id = Column(String, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    nickname = Column(String)
    numbers = Column(String(4), nullable=False)
    bot = Column(Boolean, nullable=False, default=False)

    messages = relationship("Message", foreign_keys=[Message.author])
    scores = relationship("Score", foreign_keys=[Score.member_id])
    reactions = relationship("Reaction")


class Epoch(Base):
    __tablename__ = "epoch"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    start = Column(Date, nullable=False)
    end = Column(Date, nullable=False)