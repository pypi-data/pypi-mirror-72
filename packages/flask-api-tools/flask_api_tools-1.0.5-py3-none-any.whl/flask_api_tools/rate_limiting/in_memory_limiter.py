from flask_limiter import Limiter
from flask import Flask
from typing import Any, Optional
from limits.errors import ConfigurationError


class InMemoryLimiter(Limiter):
    """
    Class extends Flask-Limiter with Redis (or any other supported in-memory storage backend)
    configuration and automatic checks
    """

    logger: Any = None

    def __init__(self, *args: Any, **kwargs: Any,) -> None:
        """
        Patch in any Flask log handlers before firing up to parent for limiter initialization
        :param app: :class:`flask.Flask` instance to initialize the extension with.
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured (via self.init_app -> invoked through superclass)
        """
        super().__init__(*args, **kwargs)

        app: Optional[Flask] = kwargs.get("app")
        if app:
            self.logger = app.logger
            for handler in app.logger.handlers:
                self.logger.debug(f"Adding log handler to limiter: {str(handler)}")
                self.logger.addHandler(handler)

    def init_app(self, app: Flask) -> None:
        """
        patch self._check_storage into Flask-limiter, and ensure the storage backend is connected properly
        app config values.
        :param app: :class:`flask.Flask` instance to initialize the extension with.
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured
        """
        super().init_app(app=app)
        self._check_storage()

    def _check_storage(self) -> None:
        """
        Check the storage backed is connected correctly
        :return: None
        :raise ConfigurationError: if storage is incorrectly configured
        """
        if not self._storage.check():
            self.logger.critical(f"Invalid storage configuration: {self._storage_uri}")
            raise ConfigurationError(
                f"Invalid storage configuration: {self._storage_uri}"
            )
