from httpx import AsyncClient  # noqa
from httpx import Client as BaseClient


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()
