
class FamilyTreeException(Exception):
    MESSAGE = 'some error in family tree'
    CODE = 1

    def __init__(self, message=None, code=None):
        self.message = message or self.MESSAGE
        self.code = code or self.CODE
        super(FamilyTreeException, self).__init__(message, code)

    def get_error_message(self):
        return self.message

    def get_error_code(self):
        return self.code


class MemberAlreadyExists(FamilyTreeException):

    MESSAGE = 'FAMILY MEMBER ALREADY EXISTS'
    CODE = 2

    def __init__(self, message=None, code=None, name=None):
        message = message if message else self.MESSAGE
        if name:
            message = '{} - {}'.format(message, name)
        super(MemberAlreadyExists, self).__init__(message, code)


class MemberNotFound(FamilyTreeException):
    MESSAGE = 'PERSON NOT FOUND'
    CODE = 3


class SpouseAlreadyExists(FamilyTreeException):
    MESSAGE = 'Spouse already exists'
    CODE = 3


class SpouseNotExist(FamilyTreeException):
    MESSAGE = 'Spouse does not exists'
    CODE = 4


class UnknownRelationship(FamilyTreeException):
    MESSAGE = 'Unknown Relationship'
    CODE = 5


class FamilyNotFound(FamilyTreeException):
    MESSAGE = 'Family Not Found'
    CODE = 6