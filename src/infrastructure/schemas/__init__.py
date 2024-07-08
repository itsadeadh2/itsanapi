from marshmallow import Schema, fields, ValidationError


class EmailSchema(Schema):
    email = fields.Email(required=True)


class MessageSchema(Schema):
    message = fields.Str(required=True)


class UserSchema(Schema):
    email = fields.Email(required=True)
    name = fields.Str(required=True)
    id = fields.Int(required=False)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class HangmanGameSchema(Schema):
    attempts_left = fields.Int(required=True)
    status = fields.Str(required=True)
    masked_word = fields.Str(required=True)
    id = fields.Int(required=True)


class HangmanGameWithSolution(HangmanGameSchema):
    solution = fields.Str(required=True)


def validate_one_char(value):
    if len(value) != 1:
        raise ValidationError("Field must be exactly one character long.")


class HangmanGuesSchema(Schema):
    guess = fields.Str(required=True, validate=validate_one_char)


class HangmanScoreSchema(Schema):
    name = fields.Str(required=True)
    score = fields.Int(required=True)
