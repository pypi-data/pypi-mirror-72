from enum import Enum
from typing import List, Optional

from pydantic import Field
from pydantic.main import BaseModel


class TelegramObject(BaseModel):
    """
    Base class for Telegram objects
    """

    pass


class User(TelegramObject):
    """
    This object represents a Telegram user or bot.
    """

    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: Optional[str]
    language_code: Optional[str]

    # below attributes returned only in `getMe()` telegram method
    can_join_groups: Optional[bool]
    can_read_all_group_messages: Optional[bool]
    supports_inline_queries: Optional[bool]


class ChatPhoto(TelegramObject):
    """
    This object represents a chat photo.
    """

    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatType(str, Enum):
    private = "private"
    group = "group"
    supergroup = "supergroup"
    channel = "channel"


class ChatPermissions(TelegramObject):
    """
    Describes actions that a non-administrator user is allowed to take in a chat.
    """

    can_send_messages: Optional[bool]
    can_send_media_messages: Optional[bool]
    can_send_polls: Optional[bool]
    can_send_other_messages: Optional[bool]
    can_add_web_page_previews: Optional[bool]
    can_change_info: Optional[bool]
    can_invite_users: Optional[bool]
    can_pin_messages: Optional[bool]


class Chat(TelegramObject):
    """
    This object represents a chat.
    """

    id: int
    type: ChatType
    title: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    photo: Optional[ChatPhoto]
    description: Optional[str]
    invite_link: Optional[str]
    pinned_message: Optional["Message"]
    permissions: Optional[ChatPermissions]
    slow_mode_delay: Optional[int]
    sticker_set_name: Optional[str]
    can_set_sticker_set: Optional[bool]


class MessageEntityType(str, Enum):
    """
    Type of the entity.
    Can be:
     - “mention” (@username),
     - “hashtag” (#hashtag),
     - “cashtag” ($USD),
     - “bot_command” (/start@jobs_bot),
     - “url” (https://telegram.org),
     - “email” (do-not-reply@telegram.org),
     - “phone_number” (+1-212-555-0123),
     - “bold” (bold text),
     - “italic” (italic text),
     - “underline” (underlined text),
     - “strikethrough” (strikethrough text),
     - “code” (monowidth string),
     - “pre” (monowidth block),
     - “text_link” (for clickable text URLs),
     - “text_mention” (for users without usernames)
    """

    mention = "mention"
    hashtag = "hashtag"
    cashtag = "cashtag"
    bot_command = "bot_command"
    url = "url"
    email = "email"
    phone_number = "phone_number"
    bold = "bold"
    italic = "italic"
    underline = "underline"
    strikethrough = "strikethrough"
    code = "code"
    pre = "pre"
    text_link = "text_link"
    text_mention = "text_mention"


class MessageEntity(TelegramObject):
    """
    This object represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.
    """

    type: MessageEntityType
    offset: int
    length: int
    url: Optional[str]
    user: Optional[User]
    language: Optional[str]


class Contact(TelegramObject):
    """
    This object represents a phone contact.
    """

    phone_number: str
    first_name: str
    last_name: Optional[str]
    user_id: Optional[int]
    vcard: Optional[str]


class Dice(TelegramObject):
    """
    This object represents an animated emoji that displays a random value.
    """

    emoji: str
    value: int


class PhotoSize(TelegramObject):
    """
    This object represents one size of a photo or a file / sticker thumbnail.
    """

    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int]


class Animation(TelegramObject):
    """
    This object represents an animation file
    (GIF or H.264/MPEG-4 AVC video without sound).
    """

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Audio(TelegramObject):
    """
    This object represents an audio file to be treated as music by the Telegram clients.
    """

    file_id: str
    file_unique_id: str
    duration: int
    performer: Optional[str]
    title: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]
    thumb: Optional[PhotoSize]


class Document(TelegramObject):
    """
    This object represents a general file
    (as opposed to photos, voice messages and audio files).
    """

    file_id: str
    file_unique_id: str
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class Point(str, Enum):
    forehead = "forehead"
    eyes = "eyes"
    mouth = "mouth"
    chin = "chin"


class MaskPosition(TelegramObject):
    """
    This object describes the position on faces where a mask should be placed by default
    """

    point: Point
    x_shift: float
    y_shift: float
    scale: float


class Sticker(TelegramObject):
    """
    This object represents a sticker.
    """

    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    thumb: Optional[PhotoSize]
    emoji: Optional[str]
    set_name: Optional[str]
    mask_position: Optional[MaskPosition]
    file_size: Optional[int]


class Video(TelegramObject):
    """
    This object represents a video file.
    """

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: Optional[PhotoSize]
    file_name: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]


class VideoNote(TelegramObject):
    """
    This object represents a video message (available in Telegram apps as of v.4.0).
    """

    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: Optional[PhotoSize]
    file_size: Optional[int]


class Voice(TelegramObject):
    """
    This object represents a voice note.
    """

    file_id: str
    file_unique_id: str
    duration: int
    mime_type: Optional[str]
    file_size: Optional[int]


class Game(TelegramObject):
    """
    This object represents a game. Use BotFather to create and
    edit games, their short names will act as unique identifiers.
    """

    title: str
    description: str
    photo: List[PhotoSize]
    text: Optional[str]
    text_entities: Optional[List[MessageEntity]]
    animation: Optional[Animation]


class PollOption(TelegramObject):
    """
    This object contains information about one answer option in a poll.
    """

    text: str
    voter_count: int


class PollType(str, Enum):
    regular = "regular"
    quiz = "quiz"


class Poll(TelegramObject):
    """
    This object contains information about a poll.
    """

    id: str
    question: str
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: PollType
    allows_multiple_answers: bool
    correct_option_id: Optional[int]
    explanation: Optional[str]
    explanation_entities: Optional[List[MessageEntity]]
    open_period: Optional[int]
    close_date: Optional[int]


class Location(TelegramObject):
    """
    This object represents a point on the map.
    """

    longitude: float
    latitude: float


class Venue(TelegramObject):
    """
    This object represents a venue.
    """

    location: Location
    title: str
    address: str
    foursquare_id: Optional[str]
    foursquare_type: Optional[str]


class Invoice(TelegramObject):
    """
    This object contains basic information about an invoice.
    """

    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class ShippingAddress(TelegramObject):
    """
    This object represents a shipping address.
    """

    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(TelegramObject):
    """
    This object represents information about an order.
    """

    name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    shipping_address: Optional[ShippingAddress]


class SuccessfulPayment(TelegramObject):
    """
    This object contains basic information about a successful payment.
    """

    currency: str
    total_amount: int
    invoice_payload: int
    shipping_option_id: Optional[int]
    order_info: Optional[OrderInfo]
    telegram_payment_charge_id: str
    provider_payment_charge_id: str


class PassportElementType(str, Enum):
    personal_details = "personal_details"
    passport = "passport"
    driver_license = "driver_license"
    identity_card = "identity_card"
    internal_passport = "internal_passport"
    address = "address"
    utility_bill = "utility_bill"
    bank_statement = "bank_statement"
    rental_agreement = "rental_agreement"
    passport_registration = "passport_registration"
    temporary_registration = "temporary_registration"
    phone_number = "phone_number"
    email = "email"


class PassportFile(TelegramObject):
    """
    This object represents a file uploaded to Telegram Passport.
    Currently all Telegram Passport files are in JPEG format when
    decrypted and don't exceed 10MB.
    """

    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int


class EncryptedPassportElement(TelegramObject):
    """
    Contains information about documents
    or other Telegram Passport elements shared with the bot by the user.
    """

    type: PassportElementType
    data: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    files: Optional[List[PassportFile]]
    front_side: Optional[PassportFile]
    reverse_side: Optional[PassportFile]
    selfie: Optional[PassportFile]
    translation: Optional[List[PassportFile]]
    hash: Optional[str]


class EncryptedCredentials(TelegramObject):
    """
    Contains data required for decrypting and authenticating EncryptedPassportElement.
    See the Telegram Passport Documentation for a complete description
    of the data decryption and authentication processes.
    """

    data: str
    hash: str
    secret: str


class PassportData(TelegramObject):
    """
    Contains information about Telegram Passport data shared with the bot by the user.
    """

    data: List[EncryptedPassportElement]
    credentials: List[EncryptedCredentials]


class LoginUrl(TelegramObject):
    """
    This object represents a parameter of the inline keyboard button used to
    automatically authorize a user. Serves as a great replacement for the
    Telegram Login Widget when the user is coming from Telegram.
    All the user needs to do is tap/click a button and confirm that they want to log in
    """

    url: str
    forward_text: Optional[str]
    bot_username: Optional[str]
    request_write_access: Optional[bool]


class CallbackGame(TelegramObject):
    """
    A placeholder, currently holds no information. Use BotFather to set up your game.
    """

    pass


class InlineKeyboardButton(TelegramObject):
    """
    This object represents one button of an inline keyboard.
    You must use exactly one of the optional fields.
    """

    text: str
    url: Optional[str]
    login_url: Optional[LoginUrl]
    callback_data: Optional[str]
    switch_inline_query: Optional[str]
    switch_inline_query_current_chat: Optional[str]
    callback_game: Optional[CallbackGame]
    pay: Optional[bool]


class InlineKeyboardMarkup(TelegramObject):
    inline_keyboard: List[List[InlineKeyboardButton]]


class Message(TelegramObject):
    """
    This class represents a message.
    """

    message_id: int
    from_user: Optional[User] = Field(alias="from")  # empty for msgs sent to channels
    date: int  # unix time
    chat: Chat
    froward_from: Optional[User]
    forward_from_chat: Optional[Chat]
    forward_from_message_id: Optional[int]
    forward_signature: Optional[str]
    forward_sender_name: Optional[str]
    forward_date: Optional[int]
    reply_to_message: Optional["Message"]
    via_bot: Optional[User]
    edit_date: Optional[int]
    media_group_id: Optional[str]
    author_signature: Optional[str]
    text: Optional[str]
    entities: Optional[List[MessageEntity]]
    animation: Optional[Animation]
    audio: Optional[Audio]
    document: Optional[Document]
    photo: Optional[List[PhotoSize]]
    sticker: Optional[Sticker]
    video: Optional[Video]
    video_note: Optional[VideoNote]
    voice: Optional[Voice]
    caption: Optional[str]
    caption_entities: Optional[List[MessageEntity]]
    contact: Optional[Contact]
    dice: Optional[Dice]
    game: Optional[Game]
    poll: Optional[Poll]
    venue: Optional[Venue]
    location: Optional[Location]
    new_chat_members: Optional[List[User]]
    left_chat_member: Optional[User]
    new_chat_title: Optional[str]
    new_chat_photo: Optional[List[PhotoSize]]
    delete_chat_photo: Optional[bool]
    group_chat_created: Optional[bool]
    supergroup_chat_created: Optional[bool]
    channel_chat_created: Optional[bool]
    migrate_to_chat_id: Optional[int]
    migrate_from_chat_id: Optional[int]
    pinned_message: Optional["Message"]
    invoice: Optional[Invoice]
    successful_payment: Optional[SuccessfulPayment]
    connected_website: Optional[str]
    passport_data: Optional[PassportData]
    reply_markup: Optional[InlineKeyboardMarkup]


class InlineQuery(TelegramObject):
    """
    This object represents an incoming inline query. When the user sends an
    empty query, your bot could return some default or trending results.
    """

    id: str
    from_user: User = Field(alias="from")
    query: str
    offset: str
    location: Optional[Location]


class ChosenInlineResult(TelegramObject):
    """
    Represents a result of an inline query that was
    chosen by the user and sent to their chat partner.
    """

    result_id: str
    from_user: User = Field(alias="from")
    inline_message_id: str
    query: str
    location: Optional[Location]


class CallbackQuery(TelegramObject):
    """
    This object represents an incoming callback query from a callback button in an
    inline keyboard. If the button that originated the query was attached to a message
    sent by the bot, the field message will be present.

    If the button was attached to a message sent via the bot (in inline mode),
    the field inline_message_id will be present.

    Exactly one of the fields data or game_short_name will be present.
    """

    id: str
    from_user: User = Field(alias="from")
    message: Optional[Message]
    inline_message_id: Optional[str]
    chat_instance: Optional[str]
    data: Optional[str]
    game_short_name: Optional[str]


class ShippingQuery(TelegramObject):
    """
    This object contains information about an incoming shipping query.
    """

    id: str
    from_user: User = Field(alias="from")
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(TelegramObject):
    """
    This object contains information about an incoming pre-checkout query.
    """

    id: str
    from_user: User = Field(alias="from")
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: Optional[str]
    order_info: Optional[OrderInfo]


class PollAnswer(TelegramObject):
    """
    This object represents an answer of a user in a non-anonymous poll.
    """

    poll_id: str
    user: User
    option_ids: List[int]


class Update(TelegramObject):
    """
    This object represents an incoming update.
    At most one of the optional parameters can be present in any given update.
    """

    update_id: int
    message: Optional[Message]
    edited_message: Optional[Message]
    channel_post: Optional[Message]
    edited_channel_post: Optional[Message]
    inline_query: Optional[InlineQuery]
    chosen_inline_result: Optional[ChosenInlineResult]
    callback_query: Optional[CallbackQuery]
    shipping_query: Optional[ShippingQuery]
    pre_checkout_query: Optional[PreCheckoutQuery]
    poll: Optional[Poll]
    poll_answer: Optional[PollAnswer]


Message.update_forward_refs()
Chat.update_forward_refs()
