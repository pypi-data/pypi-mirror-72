from pydantic import BaseModel
from typing import List, Union, Dict, Any
from enum import Enum

class EntityType(Enum):
    """https://cloud.google.com/natural-language/docs/reference/rest/v1beta2/Entity#Type"""
    UNKNOWN = "UNKNOWN"
    PERSON = "PERSON"
    LOCATION = "LOCATION"
    ORGANIZATION = "ORGANIZATION"
    EVENT = "EVENT"
    WORK_OF_ART = "WORK_OF_ART"
    CONSUMER_GOOD = "CONSUMER_GOOD"
    OTHER = "OTHER"
    PHONE_NUMBER = "PHONE_NUMBER"
    ADDRESS = "ADDRESS"
    DATE = "DATE"
    NUMBER = "NUMBER"
    PRICE = "PRICE"

class Sentiment(BaseModel):
    score: float
    magnitude: float

class Entity(BaseModel):
    name: str
    type: EntityType
    meta: Dict[str, str]
    is_named: bool
    sentiment: Sentiment
    salience: float

class Token(BaseModel):
    raw: str
    offset: int # position in the original phrase
    pos: Dict[Any, Any] # Part of Speech; Make Enum

class Language(Enum):
    en = "en"
    other = "other"

class Category(BaseModel):
    """https://cloud.google.com/natural-language/docs/categories"""
    name: str
    confidence: float

class Speech(BaseModel):
    raw: str
    tokenized: List[Token]
    stylized: str
    args: List[Entity]
    sentiment: Union[Sentiment, None]
    categories: List[Category]
    lang: Language = Language.en

class Author(BaseModel):
    is_user: bool
    _id: str

class Replic(BaseModel):
    author: Author
    timestamp: int
    speech: Speech

class SessionConfigs(BaseModel):
    local: bool = True
    visual: bool = False

class UserSettings(BaseModel):
    style: bool = False
    confirmation_threshold: float = 1.0

class UserState(BaseModel):
    dialog_skill_id: str = ""
    is_waiting: bool = False

class PublicUser(BaseModel):
    session: SessionConfigs = SessionConfigs()
    settings: UserSettings = UserSettings()
    state: UserState = UserState()

class User(PublicUser):
    token: str

class Skill(BaseModel):
    zip: str # b64
    author: Author
    name: str

class SkillInstance(BaseModel):
    skill: Skill
    state: str # b64
    user_id: str
