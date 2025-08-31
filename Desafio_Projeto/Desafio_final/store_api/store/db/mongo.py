from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings

class MongoClient:
    def __init__(self) -> None:
        # Use string para uuidRepresentation
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(
            settings.DATABASE_URL,
            uuidRepresentation="standard"  # deve ser 'standard' e não um número
        )

    def get(self) -> AsyncIOMotorClient:
        return self.client


db_client = MongoClient()