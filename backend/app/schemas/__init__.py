from marshmallow import Schema, fields, validate, EXCLUDE


class UserSchema(Schema):
    email = fields.Email()
    past_experience = fields.Str(allow_none=True)
    tech_stack = fields.List(fields.Str())
    github_profile = fields.Url(allow_none=True)
    linkedin_profile = fields.Url(allow_none=True)
    role_type = fields.Str(validate=validate.OneOf(["student", "professor", "alumni"]))
    rating = fields.Float(validate=validate.Range(min=0, max=5))

    class Meta:
        unknown = EXCLUDE


class AddProjectSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    members_required = fields.Int(required=True)
    status = fields.Str(
        validate=validate.OneOf(["Active", "Completed", "Planning"]), required=True
    )
    tags = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class FirstLoginSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class ListOfMentorsSchema(Schema):
    project_id = fields.Int(required=True)

    class Meta:
        unknown = EXCLUDE


class ApplyMentorsSchema(Schema):
    project_id = fields.Int(required=True)
    status = fields.Str(validate=validate.Equal("pending"), required=True)
    requested_at = fields.DateTime(required=True)
    remarks = fields.Str(allow_none=True)

    class Meta:
        unknown = EXCLUDE


class ApplyMentorsStatusTakebackSchema(Schema):
    project_id = fields.Int(required=True)

    class Meta:
        unknown = EXCLUDE


class AcceptMentorSchema(Schema):
    project_id = fields.Int(required=True)
    status = fields.Str(
        validate=validate.OneOf(["accepted", "rejected"]), required=True
    )


class ApplyProjectSchema(Schema):
    project_id = fields.Int(required=True)
    role = fields.Str(required=True)
    remarks = fields.Str(allow_none=True)

    class Meta:
        unknown = EXCLUDE


class ApplyProjectStatusSchema(Schema):
    project_id = fields.Int(required=True)

    class Meta:
        unknown = EXCLUDE


class ListApplyProjectSchema(Schema):
    application_id = fields.Int(required=True)
    project_id = fields.Int(required=True)
    role = fields.Str(required=True)
    status = fields.Str(required=True)
    remarks = fields.Str(allow_none=True)


class ListProjectsSchema(Schema):
    class Meta:
        unknown = EXCLUDE
