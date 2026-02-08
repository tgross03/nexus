import importlib
import warnings
from pathlib import Path

from nexus import modules
from nexus.core.config.toml import TOMLConfiguration
from nexus.core.module.module import Module


class ModuleManager:
    def __init__(self, module_config: TOMLConfiguration) -> None:
        self._modules: dict[str, Module] = {}
        self._module_config: TOMLConfiguration = module_config

    def reset_config(self) -> None:
        self._module_config.dump({"modules": []})

    def reset_modules(self) -> None:
        for module in self._modules.values():
            module.reset_config()

    def reload_modules(self) -> None:
        for module in self._modules.values():
            module.disable()

        self._modules.clear()

        load_modules = self._module_config["modules"]
        for module_path in Path(modules.__file__).parent.glob("*"):
            if not module_path.is_dir() and not module_path.name.startswith("_"):
                continue

            module_name = module_path.name

            try:
                module = importlib.import_module(
                    f".{module_name}.module", "nexus.modules"
                )

                try:
                    module_obj = getattr(module, "Module")
                except AttributeError:
                    warnings.warn(
                        f"An error occurred while loading module '{module_name}'!"
                    )
                    continue

                module_obj = module_obj(
                    config=TOMLConfiguration(
                        path=self._module_config._path.parent
                        / f"config/modules/{module_name}.toml"
                    )
                )

                if not module_obj.is_optional() or module_name in load_modules:
                    self._modules[module_obj._name] = module_obj
            except ImportError:
                continue

    def get_module(self, name: str) -> Module:
        return self._modules[name]
