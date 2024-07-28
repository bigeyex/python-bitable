from enum import Enum

class FieldType(Enum):
    Text = 1
    Number = 2
    SingleSelect = 3
    MultiSelect = 4
    DateTime = 5
    CheckBox = 7 
    User = 11
    Phone = 13
    Url = 15
    Attachment = 17
    SingleLink = 18
    Lookup = 19
    Formula = 20
    DuplexLink = 21