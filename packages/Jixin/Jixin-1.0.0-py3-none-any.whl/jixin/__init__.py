import abc
import json
from datetime import date


class JSONDecodable:
    """
    This is a mixin class to enable decoding from JSON
    It builds an internal register of candidates, and checks each of them against the
    JSON provided. If exactly one is found, it is used to decode.
    Subclasses should implement _decode_test and _decode class methods to fit their
    own purposes

    create a decoder that uses it like:

        jsondecoder = json.JSONDecoder(object_hook=JSONDecodable.object_hook)

    note: this can also be used as a stand-alone class for third party classes that
    cant be directly extended
    """

    jsondecodable = []

    # see https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls.jsondecodable.append(cls)

    @abc.abstractclassmethod
    def _decode_test(cls, dct):
        return False

    @abc.abstractclassmethod
    def _decode(cls, dct):
        raise NotImplementedError

    @classmethod
    def object_hook(cls, dct):
        # check each registered class to see if it is suitable
        cls_to_use = None
        for subcls in cls.jsondecodable:
            if subcls._decode_test(dct):
                if cls_to_use:
                    # already found a suitable class, so error
                    raise JSONDecodableConflictException(
                        f"{subcls} duplicates {cls_to_use}"
                    )
                else:
                    cls_to_use = subcls
        # if exactly one suitable class, use it
        if cls_to_use:
            return cls_to_use._decode(dct)
        else:
            return dct


class JSONDecodableConflictException(Exception):
    pass


class JSONDecodableNotFoundException(Exception):
    pass


class JSONEncoderHandler:
    @abc.abstractmethod
    def _encode_test(self, o):
        return False

    @abc.abstractmethod
    def _encode(self):
        raise NotImplementedError


class JSONEncoderDelegated(json.JSONEncoder):
    registry = []

    def __init__(self, *args, **kwargs):
        self.registry = []
        super().__init__(*args, **kwargs)

    def default(self, o):
        hander_to_use = None
        # use both class and instance handlers
        for handler in self.__class__.registry + self.registry:
            if handler._encode_test(o):
                if hander_to_use:
                    # already found a suitable class, so error
                    raise JSONEncoderDelegatedConflictException(
                        f"{handler} duplicates {hander_to_use}"
                    )
                else:
                    hander_to_use = handler
        # if exactly one suitable class, use it
        if hander_to_use:
            return hander_to_use._encode(o)
        else:
            # couldn't find a match, call superclass implementation
            return super().default(o)


class JSONEncoderDelegatedConflictException(Exception):
    pass


class JSONDEncoderDelegatedNotFoundException(Exception):
    pass


class JSONEncoderHandlerJSONEncodable(JSONEncoderHandler):
    def __init__(self, targetcls):
        self.targetcls = targetcls

    def _encode_test(self, o):
        return isinstance(o, self.targetcls)

    def _encode(self, o):
        return o._encode()

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, JSONEncoderHandlerJSONEncodable):
            return False
        return self.targetcls == other.targetcls

    def __repr__(self):
        return f"JSONEncoderHandlerJSONEncodable({self.targetcls})"


class JSONEncodable:
    """
    This is a mixin class to enable encoding to JSON
    Subclasses should implement _encode method to fit their
    own purposes
    """

    # see https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        handler = JSONEncoderHandlerJSONEncodable(cls)
        if handler not in JSONEncoderDelegated.registry:
            JSONEncoderDelegated.registry.append(handler)

    def _encode_test(self, o):
        return isinstance(o, self.__class__)

    @abc.abstractmethod
    def _encode(self):
        raise NotImplementedError


class JSONEncoderHandlerDate(JSONEncoderHandler):
    def _encode_test(self, o):
        return isinstance(o, date)

    def _encode(self, o):
        return o.isoformat()


class JSONEncoderHandlerIterable(JSONEncoderHandler):
    def _encode_test(self, o):
        try:
            iter(o)
        except TypeError:
            return False
        return True

    def _encode(self, o):
        return list(o)
