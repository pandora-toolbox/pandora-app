from dataclasses import dataclass
from typing import Optional, Dict

from src.main.sdk.models import Manifest
from src.main.sdk.plugins.arguments import PluginRuntimeArguments
from src.main.sdk.plugins.handler.command import Command


@dataclass
class PluginHandler:
    # metadata: Optional[Manifest] = None
    args: Optional[PluginRuntimeArguments] = None

    def __init__(self):
        pass
        # logging.debug(f"Initializing '{self.metadata.name}' (class '{type(self).__name__}').")

    def __call__(self):
        pass
        # if self.args is not None:
        #     pass
        #     # logging.debug(f"Executing '{self.metadata.name} {self.args.main}' (class '{type(self).__name__}').")
        # else:
        #     pass
        #     # logging.debug(f"Executing '{self.metadata.name}' (class '{type(self).__name__}').")

    @classmethod
    def commands(cls) -> Dict[str, Command]:
        return {}

    # command_spec = {
    #     "sample_command": Command(
    #         handler=None,
    #         args=[
    #             Argument(
    #                 name_or_flags=["--sample", "-s"],
    #                 help="This is a sample argument.",
    #                 action=Argument.Action.StoreString,
    #                 required=False,
    #             ),
    #             Argument(
    #                 name_or_flags=["--another", "-a"],
    #                 help="This is another sample argument.",
    #                 action=Argument.Action.StoreString,
    #                 required=True,
    #             ),
    #         ]
    #     ),
    #     "another_command": Command(
    #         handler=None,
    #         args=[
    #             Argument(
    #                 name_or_flags=["--flag"],
    #                 help="This is a boolean flag.",
    #                 action=Argument.Action.StoreBool,
    #                 required=False,
    #             ),
    #             Argument(
    #                 name_or_flags=["--number"],
    #                 help="This is a number.",
    #                 action=Argument.Action.StoreNumber,
    #                 required=True,
    #             ),
    #         ]
    #     ),
    # }

    def run(self, options: Dict[str, Command]):
        pass
        # if self.args is not None and self.args.is_present:
        #     method: Resolver = Collection.get_from(options, self.args.main)
        # 
        #     if method is not None:
        #         method.run()