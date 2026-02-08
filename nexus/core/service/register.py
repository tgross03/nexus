from __future__ import annotations

import uuid
from pathlib import Path
from typing import TYPE_CHECKING

from nexus.core.config.toml import TOMLConfiguration
from nexus.core.exceptions.services import InvalidServiceError

if TYPE_CHECKING:
    from nexus.core.service.service import Service


class ServiceRegister:
    def __init__(self) -> None:
        self._config: TOMLConfiguration = TOMLConfiguration(
            Path.home() / ".nexus/config/services.toml", create_if_not_exists=True
        )
        if "services" not in self._config:
            self._config.dump({"services": {}})

    def get_services(self) -> list[Service]:
        from nexus.core.service.service import Service

        services = []
        for unique_id, path in self._config["services"].items():
            if not Path(path).exists():
                self.unregister(unique_id=unique_id)
                continue
            services.append(Service.from_path(path=Path(path)))
        return services

    def clear(self) -> None:
        self._config.dump({})

    def register(self, service: Service) -> None:
        self._config[f"services.{str(service._uuid)}"] = str(
            service._root_dir.resolve()
        )

    def unregister(self, unique_id: uuid.UUID | str) -> None:
        self._config[f"services.{str(unique_id)}"] = None

    def get_service_by_uuid(self, unique_id: uuid.UUID | str) -> Service:
        from nexus.core.service.service import Service

        unique_id = uuid.UUID(unique_id) if isinstance(unique_id, str) else unique_id

        try:
            service = Service.from_path(self._config["services"][str(unique_id)])
        except KeyError:
            raise InvalidServiceError(
                f"There is no service registered with UUID {unique_id}"
            )

        return service

    def get_service_by_name(self, name: str) -> Service:
        for service in self.get_services():
            if service._name == name:
                return service
        raise InvalidServiceError(f"There is no service registered with name {name}!")
