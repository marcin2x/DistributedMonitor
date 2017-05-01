from abc import abstractmethod


class SensorMessage:
    type = ""

    @abstractmethod
    def get_message_body(self):
        ...

    def to_dict(self):
        return {
            "type": self.type,
            "body": self.get_message_body()
        }
