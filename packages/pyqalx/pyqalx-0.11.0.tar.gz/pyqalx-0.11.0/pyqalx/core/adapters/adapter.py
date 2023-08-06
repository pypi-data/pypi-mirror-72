import json
import os

import logging
from types import MethodType

from pyqalx.config import UserConfig, BotConfig
from pyqalx.core.entities import QalxListEntity
from pyqalx.core.errors import (
    QalxError,
    QalxNoGUIDError,
    QalxAPIResponseError,
    QalxMultipleEntityReturned,
    QalxEntityNotFound,
    QalxConfigError,
    QalxInvalidSession,
    QalxFileError,
)

logger = logging.getLogger(__name__)


class QalxAdapter(object):
    """
    The base class for a QalxAdapter. An adapter is the interface for the
    entity to the rest api.  This allows us to have a consistent interface
    across all entity types.
    Can be instatiated in two ways:

    QalxAdapter(entity_type='item') -> Returns a :class:`QalxItem` instance

    QalxItem() -> Returns a :class:`QalxItem` instance
    """

    # Certain keys shouldn't be attemped to be saved
    _keys_to_exclude = {"info", "guid", "status"}

    def __init__(self, session, *args, **kwargs):
        QalxSession = __import__("pyqalx").QalxSession
        if not isinstance(session, QalxSession):
            raise QalxInvalidSession(
                f"`qalx_session` should be an instance of"
                f" `{QalxSession}`.  "
                f"Got `{type(session)}`"
            )
        self.session = session
        super(QalxAdapter, self).__init__(*args, **kwargs)

    def __getattribute__(self, item):
        """
        Certain methods can only be called by sessions with a UserConfig or a
        BotConfig.  The API will return a 403 Permission Denied
        but this method handles showing the user a more useful error message
        """
        attr = super(QalxAdapter, self).__getattribute__(item)
        if callable(attr) and isinstance(attr, MethodType):
            # This is a method on `QalxBot`.  Check the config
            # is correct for the method we are calling
            def _msg(expected_class, actual_class):
                return (
                    f"Method `{item}` on `{self.__class__}` "
                    f"must be called via a session with a `{expected_class}`"
                    f"instance.  Got `{actual_class}`"
                )

            is_user_config = isinstance(self.session.config, UserConfig)
            is_bot_config = isinstance(self.session.config, BotConfig)

            if (
                item in getattr(self, "_user_only_methods", [])
                and not is_user_config
            ):
                raise QalxConfigError(_msg(UserConfig, BotConfig))
            if (
                item in getattr(self, "_bot_only_methods", [])
                and not is_bot_config
            ):
                raise QalxConfigError(_msg(BotConfig, UserConfig))
        return attr

    @property
    def entity_class(self):
        return self.session._registry["entities"][
            self._entity_class.entity_type
        ]

    def _process_api_request(self, method, *args, **kwargs):
        """calls to transport layer

        :param method: http method required
        :param args: args to be passed to endpoint method
        :param kwargs: kwargs to be passed to endpoint method
        :returns: `dict` containing API resource data
        """

        headers = kwargs.pop("headers", {})

        try:
            json.dumps(kwargs)
        except (TypeError, ValueError, OverflowError):
            raise QalxError(
                "One of the keyword arguments is not JSON serializable"
            )

        try:
            endpoint = getattr(self.session.rest_api, method.lower())
            logger.debug(str(endpoint))
        except AttributeError:
            raise QalxError(f"{method} not recognised.")

        success, data = endpoint(*args, json=kwargs, headers=headers)

        if success:
            return data
        m = "API request error, message:\n\n-vvv-\n\n"
        m += "\n".join([f"{k}: {v}" for k, v in data.items()])
        m += "\n\n-^^^-"
        raise QalxAPIResponseError(m)

    def detail_endpoint(self, guid, *args, **kwargs):
        """
        The endpoint for interfacing with a single
        instance of `self.entity_class`
        """
        return f"{self.entity_class.entity_type}/{guid}"

    def list_endpoint(self, *args, **kwargs):
        """
        The endpoint for interfacing with multiple instances of
        `self.entity_class`
        """
        return self.entity_class.entity_type

    @classmethod
    def get_keys_to_save(cls, entity):
        """
        When saving an entity not every key should be saved
        """
        # info & guid are both read only
        # status should only be saved via `update_status` (if available)
        return {k: entity[k] for k in entity if k not in cls._keys_to_exclude}

    @staticmethod
    def _validate(**kwargs):
        """
        Hook for specifying adapter level validation.  Returns kwargs
        so that if we need to mutate any of the kwargs (i.e. ensuring that
        a key not provided by the user has a specific value) then we can
        """
        if kwargs.get("meta", None) is None:
            # meta is optional but must always be sent through as a dict
            kwargs["meta"] = {}
        if not isinstance(kwargs["meta"], dict):
            raise QalxError("`meta` kwarg must be a `dict`")
        return kwargs

    def add(self, **kwargs):
        """
        Adds a new instance of `self.entity_class`.  Provide valid `kwargs`
        for the object you are trying to create

        :return: An instance of `self.entity_class`
        """
        if kwargs.pop("_is_validated", False) is False:
            # We may have already validated at this point if we are
            # doing a bulk insert.  This kwarg should be set on the adapter
            # that has done the validation
            kwargs = self._validate(**kwargs)
        if "tags" in kwargs.keys():
            # Ensures users don't get confused if they try to do
            # `.add(tags={'my': 'tag'}).  We cannot do this in `_validate`
            # because we only want this validation to occur on `add`
            raise QalxError(
                "Tags can only be added to entities via the "
                "session.  Do `session.tags.add(name=<tag_name>, "
                "value=<tag value>)` rather than passing a `tags` "
                "argument to `add`"
            )
        kwargs["tags"] = self.session.tags
        response = self._process_api_request(
            "post", self.list_endpoint(**kwargs), **kwargs
        )
        # TODO: #3608 Should we return packable entiies in an unpacked state?
        return self.entity_class(response)

    def get(self, guid, *args, **kwargs):
        """
        Gets an instance of `self.entity_class` by the given guid.

        :param guid: The guid of the entity to get
        :return: An instance of `self.entity_class`
        """
        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        resp = self._process_api_request("get", endpoint, *args, **kwargs)
        logger.debug(
            f"get {self.entity_class.entity_type} with "
            f"guid {guid} with {endpoint}"
        )
        return self.entity_class(resp)

    def find_one(self, query, **kwargs):
        """
        Method for returning a unique entity. Will return the entity that
        matches the query

        :param query: The mongoDB query
        :type query: dict
        :return: an instance of `self.entity_class`
        :raises: `QalxMultipleEntityReturned`
        :raises: `QalxEntityNotFound`
        """
        return self.find(many=False, limit=2, query=query, **kwargs)

    def find(
        self, query=None, sort=None, skip=0, limit=25, many=True, **kwargs
    ):
        """
        Method for listing entities.

        :param query: The optioanl Mongo query to find entities
        :param sort: The keys to sort by
        :param skip: The number of results to skip (offset) by
        :param limit: How many results should the response be limited to
        :param many: Should many entities be returned or just a single one
        :param kwargs: kwargs to query by
        :return:
        """
        list_endpoint = self.list_endpoint(**kwargs)

        logger.debug(
            f"find {self.entity_class.entity_type} with {list_endpoint}"
        )

        if query:
            # We need to dump the query to JSON as there could be
            # complex lookups which would get lost when the request is made
            try:
                query = json.dumps(query)
            except (TypeError, ValueError, OverflowError):
                raise QalxError(
                    "One of the keyword arguments is not JSON serializable"
                )

        resp = self._process_api_request(
            "get",
            list_endpoint,
            sort=sort,
            skip=skip,
            limit=limit,
            query=query,
            **kwargs,
        )
        entities = QalxListEntity(resp, child=self.entity_class)

        if many is False:

            # We are expecting only a single entity.
            entities = entities["data"]
            if len(entities) > 1:
                entities_str = "\n".join([str(q) for q in entities])
                raise QalxMultipleEntityReturned(
                    "Expected one but got "
                    "{}:\n{}".format(len(entities), entities_str)
                )
            elif entities:
                return entities[0]
            else:
                raise QalxEntityNotFound(
                    self.entity_class.entity_type + " not found."
                )
        return entities

    def reload(self, entity, *args, **kwargs):
        """
        Reloads the current entity from the API

        :return: A refreshed instance of `self.entity`
        """
        return self.get(entity["guid"], *args, **kwargs)

    def save(self, entity, *args, **kwargs):
        """
        Saves `entity` to the database.

        :return: The updated instance of `entity`
        """
        if not entity.get("guid"):
            raise QalxNoGUIDError("No guid.")
        # kwargs is also passed through as it could contain data required
        # for validation by any subclasses (blueprints/files etc)
        entity = self._validate(**entity, **kwargs)
        guid = entity["guid"]

        # If there are tags on the session then use them. Otherwise, fallback
        # to using the tags on the entity. This prevents a session without
        # tags from accidentally removing tags previously set on an entity.
        # If there are no tags on the entity (because they weren't returned via
        # `fields` then we don't update the tags - unless tags have been
        # specified on the session)
        tags_to_save = self.session.tags or entity.get("tags", None)
        if tags_to_save:
            entity["tags"] = tags_to_save

        endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        keys_to_save = self.get_keys_to_save(entity=entity)
        logger.debug(
            f"save {self.entity_class.entity_type} with "
            "guid {guid} with {endpoint}"
        )

        resp = self._process_api_request("patch", endpoint, **keys_to_save)
        return self.entity_class(resp)

    def archive(self, entity, *args, **kwargs):
        """
        Archives `entity`

        :return: The archived instance of `entity`
        """
        guid = entity["guid"]
        detail_endpoint = self.detail_endpoint(guid=guid, *args, **kwargs)
        endpoint = f"{detail_endpoint}/archive"
        logger.debug(
            f"archive {self.entity_class.entity_type} with "
            "guid {guid} with {endpoint}"
        )

        resp = self._process_api_request("patch", endpoint)
        return self.entity_class(resp)


class QalxUnpackableAdapter(QalxAdapter):
    """
    A qalx adapter for unpackable entities (Set, Group)
    """

    @property
    def kids(self):
        """
        The key that the child entities live in
        """
        return self.child_entity_class.entity_type + "s"

    @staticmethod
    def _child_list_response(child_adapter, query, **kwargs):
        return child_adapter.find(query=query)

    def _child_list_request(
        self, entity, kids, child_adapter, query_key="guid"
    ):
        """
        Builds the list request for getting any unpackable children. Handles
        chunking of the query and also pagination of the response
        :param entity: The entity that has the children
        :param kids: The details of the kids entities we want to lookup
        :param child_adapter: The child adapter to use
        :param query_key: The query key (defaults to `guid`)
        :return: A list of unpacked child_adapter.entity_class entities
        """
        unpacked_entities = []
        for _page in entity._chunks(kids, chunk_size=100):
            # Chunk to avoid hitting maximum request size
            values = list(filter(None, _page))
            query = {query_key: {"$in": values}}
            _resp = self._child_list_response(
                child_adapter=child_adapter, query=query, entity=entity
            )
            unpacked_entities += _resp["data"]
            while _resp["query"]["next"] is not None:
                # We got a paginated response so keep going through the pages
                # until we exhaust this chunk of data
                logger.debug(
                    f"get {self.entity_class.entity_type} with "
                    "{_resp['query']['next']}"
                )
                _resp = self._process_api_request("get", _resp["query"]["next"])
                unpacked_entities += QalxListEntity(
                    _resp, child=self.child_entity_class
                )["data"]
        return unpacked_entities

    def _kids_for_lookup(self, entity):
        """
        For the given entity, will get the child keys so that an API request
        can be made to obtain them
        :param entity: The entity that has child
        :return: The child keys to send to the API, as a list of values
        """
        return list(entity[self.kids].values())

    def _get_child_entities(self, entity):
        """
        Gets all the child entities for the given entity.  Handles chunking
        the children up into blocks to guard against sending a request that is
        too large.  Also handles the paginated result coming back from the
        `list` endpoint.  Does a `list` lookup for self.child_entity_class
        filtering on `guid` of the children to reduce the amount of queries

        :param entity: The entity to be unpacked
        :return: The child entities as a list
        """
        kids = self._kids_for_lookup(entity)

        child_adapter = getattr(
            self.session, self.child_entity_class.entity_type
        )
        unpacked_entities = self._child_list_request(
            entity=entity, kids=kids, child_adapter=child_adapter
        )
        return unpacked_entities

    def _unpacked_entities_to_valid_children(self, entity, unpacked_entities):
        """
        Converts a list of `unpacked_entities` into valid child entities
        for the given entity.

        :param entity: The entity that has kids that should be unpacked
        :param unpacked_entities: The unpacked child entities that need to be
                                  stitched into the entity
        :return: The unpacked entities in the correct format to be assigne to
                 `entity[self.kids]`
        """
        to_return = {}
        for key, item_guid in entity[self.kids].items():
            for child_entity in unpacked_entities:
                if item_guid == child_entity["guid"]:
                    child_entity_adapter = getattr(
                        self.session, child_entity.entity_type
                    )
                    if hasattr(child_entity_adapter, "child_entity_class"):
                        # The child entity has a child adapter of it's own.
                        # Attempt unpack. This can occur if we are unpacking
                        # a Group as we may need to unpack the Sets on the
                        # Group
                        to_return[key] = child_entity_adapter._attempt_unpack(
                            child_entity
                        )
                    else:
                        to_return[key] = child_entity
        return to_return

    def _should_unpack(self):
        return self.session.config.getboolean(
            "UNPACK_" + self.entity_class.entity_type.upper()
        )

    def _attempt_unpack(self, entity):
        """
        For the given entity will attempt
        to unpack the child_entity data that it contains

        :entity: The entity to be unpack
        :return: The entity instance with the child_entity objects unpacked
        """

        if self._should_unpack() and self.kids in entity:
            # `self.kid` might not be there if we have specified a subset
            # of fields
            unpacked_entities = self._get_child_entities(entity)
            entity[self.kids] = self._unpacked_entities_to_valid_children(
                entity=entity, unpacked_entities=unpacked_entities
            )
        return entity

    def _pack_kids_for_request(self, kwargs):
        """
        Packs the kids into a format that they need to be in
        for sending to the API
        :param kwargs: The kwargs sent to the `add` method
        :return: kwargs with packed kids
        """
        kids = {
            key: str(kid["guid"]) for key, kid in kwargs[self.kids].items()
        }  # noqa
        kwargs[self.kids] = kids
        return kwargs

    def get_keys_to_save(self, entity):
        """
        Unpackable entities will have unpacked data stored on them that have
        to be submitted as packed data
        """
        keys_to_save = super(QalxUnpackableAdapter, self).get_keys_to_save(
            entity=entity
        )
        if self.kids in keys_to_save.keys():
            keys_to_save[self.kids] = self.get_kids_keys_to_save(
                keys_to_save[self.kids]
            )
        return keys_to_save

    @staticmethod
    def get_kids_keys_to_save(kids_to_save):
        """
        Gets the keys of the kids that we want to save.  Ensures that if the
        keys are in an packed state we don't attempt to unpack them.
        :param kids_to_save: A dict of the kids we want to save
        :type kids_to_save: dict
        :return: A dict of {key:guid} of the kids we want to save
        """
        return {
            k: str(i["guid"]) if isinstance(i, dict) else i
            for k, i in kids_to_save.items()
        }

    @staticmethod
    def cache_original_kids(kids):
        """
        When saving the API only wants to know about the guids of the kids so
        we need to cache the originals
        until after the save
        :param kids: The kids on this entity
        :type kids: dict
        :return: A dictionary of the kids
        """
        return {k: v for k, v in kids.items()}

    def get(self, guid, *args, **kwargs):
        """
        Unpackable entities need to be unpacked after retrieval

        :param guid: The `guid` of the entity to get
        :return: An unpacked entity
        """
        entity = super(QalxUnpackableAdapter, self).get(
            guid=guid, *args, **kwargs
        )
        entity = self._attempt_unpack(entity)
        return entity

    def find(self, many=True, *args, **kwargs):
        entities = super(QalxUnpackableAdapter, self).find(
            many=many, *args, **kwargs
        )
        if many is False:
            # Only unpack a list view if we have a single entity
            entities = self._attempt_unpack(entities)
        return entities

    def save(self, entity, *args, **kwargs):
        """
        When saving an unpacked entity the kids need to be packed.  To save
        having to unpack them again just save the original kids and replace
        them with the packed values after saving
        """
        has_kids_key = self.kids in entity.keys()
        if has_kids_key:
            original_kids = self.cache_original_kids(entity[self.kids])

        entity = super(QalxUnpackableAdapter, self).save(
            entity=entity, *args, **kwargs
        )
        if has_kids_key:
            entity[self.kids] = original_kids
        else:
            entity = self._attempt_unpack(entity=entity)
        return entity

    def add(self, **kwargs):
        # Need to validate before we pack the kids up
        kwargs = self._validate(**kwargs)
        kwargs = self._pack_kids_for_request(kwargs)
        return super(QalxUnpackableAdapter, self).add(
            _is_validated=True, **kwargs
        )


class QalxSignalAdapter(QalxAdapter):
    """
    Bots and Workers have signals that are used to determine when to stop
    processing data.  This class provides that shared functionality
    """

    def get_signal(self, entity, *args, **kwargs):
        """
        Gets just the `signal` field from the entity and then parses that
        into the `signal_class`
        """
        entity = self.get(
            guid=entity["guid"], fields="signal", *args, **kwargs
        )  # noqa
        signal = self.signal_class(entity)
        return signal

    def terminate(self, entity, *args, **kwargs):
        """
        Updates the entity with a terminate signal
        """
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        logger.debug(
            f"terminate {self.entity_class.entity_type} with guid {guid} with {endpoint}"  # noqa
        )
        signal = self.signal_class._terminate_signal(*args, **kwargs)

        self._process_api_request("patch", endpoint, signal=signal)

    def _stop_or_resume(self, entity, stop, **kwargs):
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        signal = self.signal_class._stop_signal(stop)
        logger.debug(
            f"signal {signal} {self.entity_class.entity_type} with guid {guid} with {endpoint}"  # noqa
        )
        self._process_api_request("patch", endpoint, signal=signal)

    def stop(self, entity, **kwargs):
        """
        Updates the entity with a stop signal
        """
        self._stop_or_resume(entity, stop=True, **kwargs)

    def resume(self, entity, **kwargs):
        """
        Updates the entity with a resume signal
        """
        self._stop_or_resume(entity, stop=False, **kwargs)


class QalxNamedEntityAdapter(QalxAdapter):
    """
    Certain QalxEntities have a `name` field that can be used to look up the
    entity.
    """

    def get_by_name(self, name):
        """a single entity by name

        :param name: name of entity
        :type name: str
        :return: instance of `self.entity_class`
        :raises: pyqalx.errors.QalxReturnedMultipleError,
                 pyqalx.errors.QalxEntityNotFound
        """
        return self.find_one(query={"name": name})

    def get_or_create(self, name, meta=None, **kwargs):
        """
        Gets an Entity by the given name or creates it if it doesn't exist

        :param name: The `name` that to use to get or create the entity by
        :type name: str
        :param meta: metadata about the entity
        :param kwargs: Other kwargs on the entity to use when creating
        :return: instance of `self.entity_class`
        """
        try:
            return self.get_by_name(name=name)
        except QalxEntityNotFound:
            return self.add(name=name, meta=meta, **kwargs)


class QalxValidateBlueprintAdapter(QalxAdapter):
    """
    Certain entity types can be validated against a preexisting Blueprint
    when they are created.
    """

    def _validate(self, blueprint_name=None, **kwargs):
        """
        When adding entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are creating
        the entity with

        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :param get_blueprint: Should this method retrieve the blueprint?
        :type get_blueprint: bool, False
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        validated_data = super(QalxValidateBlueprintAdapter, self)._validate(
            **kwargs
        )
        if blueprint_name is not None:
            blueprint = validated_data.pop("blueprint", None)
            if blueprint is None:
                blueprint = self._get_blueprint(name=blueprint_name)
            blueprint.validate(validated_data)
        return validated_data

    def _get_blueprint(self, name):
        """
        Helper method for getting the blueprint instance
        :param name: The name of the blueprint
        :type name: str
        :return: A `~entities.blueprint.Blueprint` instance
        """
        blueprint = self.session.blueprint.get_by_name(name=name)
        return blueprint

    def add(self, blueprint_name, **kwargs):
        """
        When adding entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are creating
        the entity with

        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        return super(QalxValidateBlueprintAdapter, self).add(
            blueprint_name=blueprint_name, **kwargs
        )

    def save(self, entity, blueprint_name=None, *args, **kwargs):
        """
        When saving entities that inherit from this class, pyqalx will get
        the blueprint based on the `blueprint_name` and then ensure that
        the schema validates correctly against the data that you are updating
        the entity with
        :param entity: The entity instance that you are saving
        :type entity: entities.QalxEntity instance
        :param blueprint_name: the name of the blueprint
        :type blueprint_name: str, None
        :return: A valid `self.entity_class` instance
        :raises: jsonschema.ValidationError
        """
        return super(QalxValidateBlueprintAdapter, self).save(
            entity, blueprint_name=blueprint_name, **kwargs
        )


class QalxFileAdapter(QalxAdapter):
    """
    Adapter that allows files to be uploaded to an entity
    """

    def _validate(self, input_file, file_name, **kwargs):
        """
        Ensures that the `input_file` and/or `file_name` are present
        and correct
        :param input_file: The path to the file or the file stream
        :param file_name: The name of the file
        :return: kwargs
        """
        if input_file is not None:
            # Only validate the file is it's specified in the
            # implementing adapter
            is_filestream = self.session.rest_api.is_filestream(input_file)
            if is_filestream:
                if not file_name:
                    raise QalxFileError(
                        "You must supply a file name when supplying"
                        " a file stream"
                    )
                file = {"name": file_name}
            else:
                if os.path.isfile(input_file):
                    file_path = os.path.abspath(input_file)
                    filename = (
                        file_name if file_name else os.path.basename(file_path)
                    )
                    file = {"name": filename}
                else:
                    raise QalxFileError(
                        "Invalid file `{0}`".format(input_file)
                    )  # noqa
            kwargs[self.entity_class._file_key] = file
        return super(QalxFileAdapter, self)._validate(**kwargs)

    def add(self, input_file, file_name, upload=True, **kwargs):
        """
        When a user creates an entity with a file pyqalx will upload the file
        automatically for you after the entity itself has been created.  Pass
        `upload=False` through to stop this from happening and upload the file
        yourself
        :param input_file: The input file path or stream
        :param file_name: The optional file name
        :param upload: Whether the file should be automatically uploaded or not
        :return: A valid entity
        """
        entity = super(QalxFileAdapter, self).add(
            input_file=input_file, file_name=file_name, **kwargs
        )
        if upload and input_file is not None:
            entity = self._upload_file(entity=entity, input_file=input_file)
        return entity

    def save(
        self, entity, input_file, file_name, upload=True, *args, **kwargs
    ):  # noqa
        """
        Saves an entity - optionally updating any file data.
        :param entity: The entity that is being saved
        :param input_file: The input file path or stream
        :param file_name: The optional file name
        :param upload: Whether the file should be automatically uploaded or not
        :return: A valid entity
        """
        entity = super(QalxFileAdapter, self).save(
            entity=entity, input_file=input_file, file_name=file_name, **kwargs
        )
        if input_file is not None:
            if upload:
                entity = self._upload_file(
                    entity=entity, input_file=input_file
                )  # noqa
            else:
                # Entity is returned with the put_url so that the user can
                # upload the file manually
                return entity
        # Ensure "put_url" is removed even if we are not changing the file
        entity[self.entity_class._file_key].pop("put_url", None)
        return entity

    def _upload_file(self, entity, input_file):
        # Only upload if everything was OK with the item creation
        # and the user wants to upload the file automatically.
        s3_resp_ok, s3_data = self.session.rest_api._upload_to_s3(
            entity, input_file, self.entity_class._file_key
        )  # noqa
        if s3_resp_ok is False:
            # The S3 upload failed, return the failed S3 response in place
            # of the response from the api.  Any implementing client will
            # have to handle tidying up any incorrect data.
            # TODO: #3928 Handle errors in a consistent way in adapters
            m = "API request error, message:\n\n-vvv-\n\n"
            m += "\n".join([f"{k}: {v}" for k, v in s3_data.items()])
            m += "\n\n-^^^-"
            raise QalxAPIResponseError(m)
        else:
            # Always pop the `put_url` off if it's a success
            entity[self.entity_class._file_key].pop("put_url")
        return entity


class QalxUpdateStatusAdapter(QalxAdapter):
    def update_status(self, entity, status, **kwargs):
        """
        Updates the status of an entity

        :param entity: The entity that is being updated
        :type entity: An instance of ~entities.entity.QalxEntity
        :param status: The status to update to
        :type: status: str
        """
        guid = entity["guid"]
        endpoint = self.detail_endpoint(guid=guid, **kwargs)
        logger.debug(
            f"update status{self.entity_class.entity_type} with guid {guid} with {endpoint}"  # noqa
        )
        status_dict = {"message": status}
        self._process_api_request("patch", endpoint, status=status_dict)
