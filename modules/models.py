from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Float, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base, Mapped
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = Column(Integer, primary_key=True)
    tg_id: Mapped[int] = Column(BigInteger, unique=True)
    name: Mapped[str] = Column(String)

class Account(Base):
    __tablename__ = 'account'
    id: Mapped[int] = Column(Integer, primary_key=True)
    account_id: Mapped[int] = Column(BigInteger, unique=True)
    account_oid: Mapped[str] = Column(String)
    account_name: Mapped[str] = Column(String)
    full_name: Mapped[str] = Column(String)
    avatar: Mapped[str] = Column(String, nullable=True)
    live_ads: Mapped[int] = Column(Integer, nullable=True)
    
    # Relationship
    ads = relationship("Ad", back_populates="account")

class Ad(Base):
    __tablename__ = 'ad'
    id: Mapped[int] = Column(Integer, primary_key=True)
    ad_id: Mapped[int] = Column(BigInteger, unique=True)
    list_id: Mapped[int] = Column(BigInteger)
    list_time: Mapped[int] = Column(BigInteger)
    state: Mapped[str] = Column(String)
    type: Mapped[str] = Column(String)
    region: Mapped[int] = Column(Integer)
    category: Mapped[int] = Column(Integer)
    subject: Mapped[str] = Column(String)
    body: Mapped[str] = Column(Text)
    image: Mapped[str] = Column(String, nullable=True)
    status: Mapped[str] = Column(String)
    commercial_type: Mapped[int] = Column(Integer, nullable=True)
    size: Mapped[int] = Column(Integer, nullable=True)
    area: Mapped[int] = Column(Integer, nullable=True)
    longitude: Mapped[float] = Column(Float, nullable=True)
    latitude: Mapped[float] = Column(Float, nullable=True)
    property_legal_document: Mapped[int] = Column(Integer, nullable=True)
    region_v2: Mapped[int] = Column(Integer, nullable=True)
    area_v2: Mapped[int] = Column(Integer, nullable=True)
    ward: Mapped[int] = Column(Integer, nullable=True)
    furnishing_sell: Mapped[int] = Column(Integer, nullable=True)
    street_name: Mapped[str] = Column(String, nullable=True)
    location_id: Mapped[str] = Column(String, nullable=True)
    unique_street_id: Mapped[str] = Column(String, nullable=True)
    is_main_street: Mapped[bool] = Column(Boolean, nullable=True)
    location: Mapped[str] = Column(String, nullable=True)
    date: Mapped[str] = Column(String, nullable=True)
    category_name: Mapped[str] = Column(String, nullable=True)
    area_name: Mapped[str] = Column(String, nullable=True)
    region_name: Mapped[str] = Column(String, nullable=True)
    price_string: Mapped[str] = Column(String, nullable=True)
    webp_image: Mapped[str] = Column(String, nullable=True)
    number_of_images: Mapped[int] = Column(Integer, nullable=True)
    ward_name: Mapped[str] = Column(String, nullable=True)
    pty_map: Mapped[str] = Column(String, nullable=True)
    pty_map_modifier: Mapped[float] = Column(Float, nullable=True)
    thumbnail_image: Mapped[str] = Column(String, nullable=True)
    size_unit_string: Mapped[str] = Column(String, nullable=True)
    contain_videos: Mapped[int] = Column(Integer, nullable=True)
    
    # Foreign key
    account_id_fk: Mapped[int] = Column(Integer, ForeignKey('account.id'))
    
    # Relationships
    account = relationship("Account", back_populates="ads")
    images = relationship("AdImage", back_populates="ad", cascade="all, delete-orphan")
    parameters = relationship("AdParameter", back_populates="ad", cascade="all, delete-orphan")
    
    # Timestamps
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Statuses:
    posted: Mapped[datetime] = Column(DateTime, default=None, nullable=True)
    translated: Mapped[bool] = Column((Boolean), default=False)

class AdImage(Base):
    __tablename__ = 'ad_image'
    id: Mapped[int] = Column(Integer, primary_key=True)
    ad_id_fk: Mapped[int] = Column(Integer, ForeignKey('ad.id'))
    image_url: Mapped[str] = Column(String)
    thumbnail_url: Mapped[str] = Column(String, nullable=True)
    image_type: Mapped[str] = Column(String, default='regular')  # regular, thumbnail, webp
    
    # Relationship
    ad = relationship("Ad", back_populates="images")

class AdParameter(Base):
    __tablename__ = 'ad_parameter'
    id: Mapped[int] = Column(Integer, primary_key=True)
    ad_id_fk: Mapped[int] = Column(Integer, ForeignKey('ad.id'))
    param_id: Mapped[str] = Column(String)
    value: Mapped[str] = Column(String)
    label: Mapped[str] = Column(String)
    
    # Relationship
    ad = relationship("Ad", back_populates="parameters")

