from typing import Optional, List

from pydantic import BaseModel, Field


class Chat(BaseModel):
    last_name: Optional[str]
    id: Optional[int]
    type: Optional[str]
    first_name: Optional[str]
    username: Optional[str]


class From(BaseModel):
    last_name: Optional[str]
    id: Optional[int]
    first_name: Optional[str]
    user_name: Optional[str]
    language_code: Optional[str]
    is_bot: Optional[str]


class ReplyMessage(BaseModel):
    date: Optional[int]
    chat: Optional[Chat]
    message_id: Optional[int]
    text: Optional[str]


class File(BaseModel):
    file_id: Optional[str]


class Message(BaseModel):
    date: Optional[int]
    chat: Optional[Chat]
    message_id: Optional[str]
    from_field: From = Field(alias="from")
    forward_date: Optional[int]
    text: Optional[str]
    photo: Optional[List[File]]
    document: Optional[File]
    video: Optional[File]
    video_note: Optional[File]
    voice: Optional[File]


class ChatGroup(BaseModel):
    id: Optional[int]
    title: Optional[str]
    type: Optional[str]


class MockVal(BaseModel):
    rand_int: Optional[int]


class OtherChatMember(BaseModel):
    user: Optional[From]
    status: Optional[str]


class MyChatMember(BaseModel):
    rand_int: Optional[int]
    chat: Optional[ChatGroup]
    from_field: Optional[From] = Field(alias="from")
    date: Optional[int]
    old_chat_member: Optional[OtherChatMember]
    new_chat_member: Optional[OtherChatMember]


class MessageBodyModel(BaseModel):
    update_id: Optional[int]
    message: Optional[Message]
    my_chat_member: Optional[MyChatMember]
    reply_to_message: Optional[ReplyMessage]


class ResponseToMessage(BaseModel):
    method: Optional[str] = "sendMessage"
    chat_id: Optional[int] = 861126057
    from_chat_id: Optional[int]
    message_id: Optional[int]
    text: Optional[str]
    photo: Optional[str]
    document: Optional[str]
    parse_mode: Optional[str] = "Markdown"
