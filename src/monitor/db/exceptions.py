class MissingParameterException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class NameDuplicatedException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MeasurementNotFoundException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class MeasurementIsNotComplexException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserNotAllowedToDeleteException(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

