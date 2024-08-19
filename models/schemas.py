from models import ma
from models.user import User
from models.address import Address
from models.phone_number import PhoneNumber

class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address

class PhoneNumberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PhoneNumber

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        