from http import HTTPStatus

class AppException(Exception): 
    def __init__(self, status_code: int, detail: str): 
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class CategoryNotFoundException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "Category not found.")

class ProductNotFoundException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "Product not found.")

class SameSkuException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.CONFLICT, "This SKU is already used by another product.")

class DuplicatedCategoryException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.CONFLICT, "Category is already linked to this product.")

class UnlinkedCategoryException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, "Product is not linked to this category.")

class CategoryNameAlreadyExists(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.CONFLICT, "A category with this name already exists.")

class UserNotFoundException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.NOT_FOUND, "User not found.")

class InvalidTokenException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Invalid token.")

class UnauthorizedException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Unauthorized access.")

class InvalidPasswordException(AppException): 
    def __init__(self):
        super().__init__(HTTPStatus.BAD_REQUEST, "Invalid password.")
