def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


#reference is from https://github.com/nesdis/djongo/issues/298
# MongoDB codex packages; should be available in most python distributions
from bson import ObjectId
from bson.errors import InvalidId
from rest_framework import serializers

class ObjectIdField(serializers.Field):
    
    """ Serializer field for Djongo ObjectID fields """
    
    def to_internal_value(self, data):
        # Serialized value -> Database value
        try:
            return ObjectId(str(data))  # Get the ID, then build an ObjectID instance using it
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data)
            )
    
              
    def to_representation(self, value):
        # Database value -> Serialized value
        if not ObjectId.is_valid(value):  # User submitted ID's might not be properly structured
            raise InvalidId
        return smart_text(value)
