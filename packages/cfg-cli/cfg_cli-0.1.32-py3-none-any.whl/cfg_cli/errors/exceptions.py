class CofactorError(Exception):
    """
    Base class for exceptions
    """

    message = ""
    code = ""

    def __str__(self):
        return f"{self.__class__.__name__} - {self.message}"


class NotLoggedIn(CofactorError):
    message = "Please use the login command to authenticate your request."
    code = 400


class InvalidCredentials(CofactorError):
    message = "Invalid or expired credentials provided, please try logging again."
    code = 401
