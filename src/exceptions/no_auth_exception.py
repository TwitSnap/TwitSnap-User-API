class UnauthorizedException(RuntimeError):
    def __init__(self, detail):
        self.detail = detail
        super().__init__(detail)
