class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code
        
class CategoryNotFoundException(AppException): 
    pass

class ProductNotFoundException(AppException): 
    pass

class SameSkuException(AppException): 
    pass

class SameSkuException(AppException): 
    pass

class DuplicatedCategoryException(AppException): 
    pass

class UnlinkedCategoryException(AppException): 
    pass

class CategoryNameAlreadyExists(AppException): 
    pass

class UserNotFoundException(AppException): 
    pass

class InvalidTokenException(AppException): 
    pass

class UnauthorizedException(AppException): 
    pass

class InvalidPasswordException(AppException):
    pass