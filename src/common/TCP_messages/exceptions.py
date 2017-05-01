class SensorMonitorCommunicationException(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return self.message


class MissingMessageParameterException(SensorMonitorCommunicationException):
    def __init__(self, parameter):
        self.message = "Missing required parameter: \"%s\"" % parameter


class MissingSensorRegisterRequestParameterException(MissingMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MissingSensorDataRequestParameterException(MissingMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MissingSensorRegisterResponseParameterException(MissingMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MissingSensorDataResponseParameterException(MissingMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidMessageParameterException(SensorMonitorCommunicationException):
    def __init__(self, message):
        self.message = message


class InvalidSensorRegisterRequestParameterException(InvalidMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSensorDataRequestParameterException(InvalidMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSensorRegisterResponseParameterException(InvalidMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSensorDataResponseParameterException(InvalidMessageParameterException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class InvalidSensorMessageTypeException(SensorMonitorCommunicationException):
    def __init__(self, request_type):
        self.message = "Invalid sensor request type: \"%s\"" % request_type
