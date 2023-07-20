import sys
sys.path.append('..')

from typing import Union
import pydantic

class NoteSchema(pydantic.BaseModel):
    title: Union[str, None] = ''
    description: Union[str, None] = ''

import peewee
import datetime
from uuid import uuid4

from utils.database import BaseModel, conn

class Note(BaseModel):
    id = peewee.UUIDField(primary_key=True, default=uuid4)
    title = peewee.TextField(default='')
    description = peewee.TextField(default='')
    createdAt = peewee.DateTimeField(default=datetime.datetime.now)

conn.create_tables([Note])