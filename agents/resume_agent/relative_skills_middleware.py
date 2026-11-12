from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from langchain.agents.middleware import AgentMiddleware, AgentState, ContextT, ResponseT
from langchain.agents.middleware.types import PrivateStateAttr

if TYPE_CHECKING:
    from deepagents.backends import BACKEND_TYPES


class RelativeSkillsMiddleware(AgentMiddleware[AgentState, ContextT, ResponseT]):
    """Middleware for loading skills from relative paths within the project."""
    
    def __init__(
        self,
        backend: "BACKEND_TYPES",
        skills_dir: str,
    ):
        from engine.core.configs import Config
        
        super().__init__()
        self._backend = backend
        self._skills_dir = Path(Config.WORKSPACE_ROOT) / skills_dir
        self._sources = [f"/{skills_dir}"]
    
    @property
    def sources(self) -> list[str]:
        return self._sources
    
    @property
    def backend(self) -> "BACKEND_TYPES":
        return self._backend
    
    async def abefore_agent(self, state: AgentState, runtime) -> None:
        from deepagents.middleware.skills import SkillsMiddleware
        from deepagents.backends.filesystem import FilesystemBackend
        
        backend = FilesystemBackend(root_dir=str(Path(self._skills_dir).parent))
        
        middleware = SkillsMiddleware(
            backend=backend,
            sources=self._sources,
        )
        
        state["middleware"] = state.get("middleware", []) + [middleware]