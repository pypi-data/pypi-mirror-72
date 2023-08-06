import os
from itertools import zip_longest

import requests

from pyqalx.core.entities.object_dict import ObjectDict

from pyqalx.core.errors import (
    QalxAPIResponseError,
    QalxEntityTypeNotFound,
    QalxError,
)


class QalxListEntity(ObjectDict):
    """
    Simple wrapper around a pyqalxapi_dict so we can keep extra keys
    on the API list response.  Instantiates each entity in `data` to the
    correct QalxEntity subclass.
    """

    _data_key = "data"

    def __new__(cls, pyqalxapi_list_response_dict, *args, **kwargs):
        """
        A QalxListEntity is just an ObjectDict that has a list of
        QalxEntity instances stored on the `_data_key`.
        :param pyqalxapi_list_response_dict: A dict that gets returned from
        a pyqalxapi list endpoint.  This should at minimum have a `data`
        key but may have other keys which we preserve
        :param kwargs: Must contain `child` key which is a subclass of `QalxEntity`

        """
        cls.child = kwargs["child"]

        if not issubclass(cls.child, (QalxEntity,)):
            raise QalxEntityTypeNotFound(
                f"Expected `child` to be a subclass of "
                f"`QalxEntity`.  Got `{cls.child}`"
            )

        return super(QalxListEntity, cls).__new__(
            cls, pyqalxapi_list_response_dict
        )

    def __init__(self, pyqalxapi_list_response_dict, *args, **kwargs):
        super().__init__(pyqalxapi_list_response_dict)

        if (
            self._data_key not in pyqalxapi_list_response_dict
            or not isinstance(
                pyqalxapi_list_response_dict[self._data_key], list
            )
        ):
            raise QalxAPIResponseError(
                "Expected `{0}` key in "
                "`pyqalxapi_list_response_dict` and for"
                " it to be a list".format(self._data_key)
            )
        # Cast all the entities in data to be an instance of `self.child`
        self[self._data_key] = [
            self.child(e) for e in pyqalxapi_list_response_dict[self._data_key]
        ]  # noqa

    def __str__(self):
        return f"[{self.child.entity_type} list]"


class QalxEntity(ObjectDict):
    """Base class for qalx entities_response.

    QalxEntity children need to be populated with either a
    `requests.models.Response` which is the type returned by the methods
    on `pyqalxapi.api.PyQalxAPI` or with a `dict`.

    Entities can behave either like a dict or attribute lookups can be used
    as getters/setters

    >>> class AnEntity(QalxEntity):
    ...     pass
    >>> c = AnEntity({"guid":"123456789", "info":{"some":"info"}})
    >>> # dict style lookups
    >>> c['guid']
    '123456789'
    >>> # attribute style lookups
    >>> c.guid
    '123456789'


    :param pyqalxapi_dict: a 'dict' representing a qalx entity object to
        populate the entity
    :type pyqalxapi_dict: dict
    """

    entity_type: str

    def __init__(self, pyqalxapi_dict):
        super().__init__(pyqalxapi_dict)

    def __str__(self):
        return f"[{self.entity_type}] {self['guid']}"

    @classmethod
    def _chunks(cls, _iterable, chunk_size, fillvalue=None):
        """
        Collect data into fixed-length chunks or blocks"
        # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
        Taken from the itertools documentation
        """
        args = [iter(_iterable)] * chunk_size
        return zip_longest(fillvalue=fillvalue, *args)

    def __super_setattr__(self, name, value):
        """
        Convenience method for setting proper attributes on the entity class.
        Because we are using `ObjectDict` if we did
        `self.<name> = value` this would set the
        dict key of `<name>` which we don't want.  So we call
        the supermethod to properly set the attribute
        :param name: The name of the attribute to set
        :param value: The value of the attribute to set
        """
        super(ObjectDict, self).__setattr__(name, value)

    def __dir__(self):
        """
        By default `ObjectDict` __dir__ only returns the keys on the dict.
        We want it to return everything as normal as entities might have
        methods that the user needs to know about
        """
        return super(ObjectDict, self).__dir__()


class QalxFileEntity(QalxEntity):
    _file_bytes = None
    _file_key = "file"

    def read_file(self):
        """
        If this Item contains a file, will read the file data and cache it
        against the Item.

        :return: The content of the URL as a bytes object.  Accessible from
            the `_file_bytes` attribute
        :raises: pyqalx.errors.QalxError
        """
        if not self.get(self._file_key):
            raise QalxError("Item doesn't have file data.")
        else:
            response = requests.get(url=self[self._file_key]["url"])
            if response.ok:
                self.__super_setattr__("_file_bytes", response.content)
                return self._file_bytes
            else:
                raise QalxError(
                    "Error with file retrieval: \n\n" + response.text
                )

    def save_file_to_disk(self, filepath, filename=None):
        """
        If this Item contains a file, will read the file from the URL (or from
        the cached bytes on the instance) and save the file to disk.  Provide
        an optional `filename` argument if you don't want to use the same
        filename as the one stored on the Item

        :param filepath: The path where this file should be saved
        :type filepath: str
        :param filename: The optional name of this file. Defaults to the name
            of the file on the instance
        :type filename: str
        :raises: pyqalx.errors.QalxError
        """
        if filename is None:
            filename = self[self._file_key]["name"]
        if self._file_bytes is None:
            self.read_file()
        _filepath = os.path.join(filepath, filename)
        with open(_filepath, "wb") as f:
            f.write(self._file_bytes)
        return _filepath
