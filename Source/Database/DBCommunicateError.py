class DBCommunicateError(Exception):
    # Error Unknow - 0
    # Error Database connection - 1/9
    # Error Content - 10/19
    # Error Users - 20/29
    # Error Mood - 30/39
    # Error UsersTaste - 40/49
    # Error Commit - 100/109

    def __init__(self, message: str, code: int = None):
        super().__init__(message)

        self.ERRORS = {
            0: "",

        }

        self.message = message
        self.code = code

    def __str__(self):
        return f"{self.message}: [{self.code}]" if self.code else self.message