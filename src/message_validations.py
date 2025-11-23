from typing import Optional, List, Any

from pydantic import BaseModel, Field, ConfigDict


class Chat(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    last_name: Optional[str] = None
    id: Optional[int] = None
    type: Optional[str] = None
    first_name: Optional[str] = None
    username: Optional[str] = None


class From(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    last_name: Optional[str] = None
    id: Optional[int] = None
    first_name: Optional[str] = None
    user_name: Optional[str] = None
    username: Optional[str] = None  # Telegram uses 'username' not 'user_name'
    language_code: Optional[str] = None
    is_bot: Optional[bool] = None  # Telegram sends bool, not string


class ReplyMessage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    date: Optional[int] = None
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    text: Optional[str] = None


class File(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    file_id: Optional[str] = None


class NewChatMember(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: Optional[int] = None


class Message(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    date: Optional[int] = None
    chat: Optional[Chat] = None
    message_id: Optional[int] = None  # Telegram sends int, not string
    from_field: Optional[From] = Field(default=None, alias="from")
    forward_date: Optional[int] = None
    text: Optional[str] = None
    photo: Optional[List[File]] = None
    document: Optional[File] = None
    video: Optional[File] = None
    video_note: Optional[File] = None
    voice: Optional[File] = None
    new_chat_member: Optional[NewChatMember] = None
    left_chat_member: Optional[NewChatMember] = None
    group_chat_created: Optional[bool] = None


class ChatGroup(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    id: Optional[int] = None
    title: Optional[str] = None
    type: Optional[str] = None


class MockVal(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    rand_int: Optional[int] = None


class OtherChatMember(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    user: Optional[From] = None
    status: Optional[str] = None


class MyChatMember(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    rand_int: Optional[int] = None
    chat: Optional[ChatGroup] = None
    from_field: Optional[From] = Field(default=None, alias="from")
    date: Optional[int] = None
    old_chat_member: Optional[OtherChatMember] = None
    new_chat_member: Optional[OtherChatMember] = None


class MessageBodyModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    
    update_id: Optional[int] = None
    message: Optional[Message] = None
    my_chat_member: Optional[MyChatMember] = None
    reply_to_message: Optional[ReplyMessage] = None


class ResponseToMessage(BaseModel):
    method: Optional[str] = "sendMessage"
    chat_id: Optional[int] = 861126057
    from_chat_id: Optional[int] = None
    message_id: Optional[int] = None
    text: Optional[str] = None
    photo: Optional[str] = None
    document: Optional[str] = None
    parse_mode: Optional[str] = "Markdown"
    disable_notification: Optional[bool] = None
