from marshmallow import Schema, fields, validate, validates, ValidationError
from flask_smorest.fields import Upload


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(dump_only=True)


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
    file = Upload()

    @validates("file")
    def validate_file(self, data):
        file_name = data.filename.lower()
        print(data, data.__dict__)
        if not file_name.endswith(".csv"):
            raise ValidationError("Only CSV files are allowed.")

        return True


class UserRoleSchema(Schema):
    role = fields.Str(
        validate=validate.OneOf(["user", "admin", "manager", "analyst", "worker"]),
        required=True,
    )


class ProductionDataSchema(Schema):
    req_finish_fabrics = fields.Float(required=True)
    fabric_allowance = fields.Float(required=True)
    rec_beam_length_yds = fields.Float(required=True)
    shrink_allow = fields.Float(required=True)
    req_grey_fabric = fields.Float(required=True)
    req_beam_length_yds = fields.Float(required=True)
    total_pdn_yds = fields.Float(required=True)
    rejection = fields.Float(required=True)
    warp_count = fields.Float(required=True)
    weft_count = fields.Float(required=True)
    epi = fields.Integer(required=True)
    ppi = fields.Integer(required=True)


class ProductionReportSchema(ProductionDataSchema):
    id = fields.Int(dump_only=True)


class ConstructionSchema(Schema):
    warp_count = fields.Integer(required=True)
    weft_count = fields.Integer(required=True)
    epi = fields.Integer(required=True)
    ppi = fields.Integer(required=True)


class LogSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str()
    timestamp = fields.DateTime()

    user = fields.Nested(UserSchema)
