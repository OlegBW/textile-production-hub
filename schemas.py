from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class PredictionInputSchema(Schema):
    req_finish_fabrics = fields.Float(required=True, load_only=True)
    fabric_allowance = fields.Float(required=True, load_only=True)
    rec_beam_length_yds = fields.Float(required=True, load_only=True)
    shrink_allow = fields.Float(required=True, load_only=True)
    req_grey_fabric = fields.Float(required=True, load_only=True)
    req_beam_length_yds = fields.Float(required=True, load_only=True)
    total_pdn_yds = fields.Float(required=True, load_only=True)
    warp_count = fields.Float(required=True, load_only=True)
    weft_count = fields.Float(required=True, load_only=True)
    epi = fields.Int(required=True, load_only=True)
    ppi = fields.Int(required=True, load_only=True)


class PredictionBulkSchema(Schema):
    file = fields.Raw(type="file")


# Додати валідації файлу
