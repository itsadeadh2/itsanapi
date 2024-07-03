from marshmallow import Schema, fields


class EmailSchema(Schema):
    email = fields.Email(required=True)


class MessageSchema(Schema):
    message = fields.Str(required=True)


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
