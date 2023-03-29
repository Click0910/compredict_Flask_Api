from marshmallow import Schema, fields, ValidationError


class StandardizationRequestSchema(Schema):
    signals = fields.List(fields.List(fields.Float()), required=True)


class StandardizationResponseSchema(Schema):
    signals = fields.List(fields.List(fields.Float()), required=True)