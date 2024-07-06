from marshmallow import Schema, fields


class EmailSchema(Schema):
    email = fields.Email(required=True)


class MessageSchema(Schema):
    message = fields.Str(required=True)


class UserSchema(Schema):
    email = fields.Str(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=False)
