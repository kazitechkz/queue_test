from fastapi import HTTPException, status


class AppExceptionResponse:
    @staticmethod
    def bad_request(message: str = "Bad request"):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    @staticmethod
    def unauthorized(message: str = "Unauthorized"):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    @staticmethod
    def forbidden(message: str = "Forbidden"):
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

    @staticmethod
    def not_found(message: str = "Resource not found"):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    @staticmethod
    def conflict(message: str = "Conflict occurred"):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)

    @staticmethod
    def internal_error(message: str = "Internal server error"):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
        )
