from typing import List, Optional
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException


class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        try:
            await self.collection.insert_one(product_model.model_dump())
        except PyMongoError as e:
            raise InsertErrorException(f"Erro ao inserir produto: {str(e)}")

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self, min_price: Optional[float] = None, max_price: Optional[float] = None) -> List[ProductOut]:
        filter_dict = {}

        if min_price is not None or max_price is not None:
            filter_dict["price"] = {}
            if min_price is not None:
                filter_dict["price"]["$gt"] = min_price
            if max_price is not None:
                filter_dict["price"]["$lt"] = max_price

        cursor = self.collection.find(filter_dict)
        return [ProductOut(**item) async for item in cursor]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        # garante que updated_at sempre será atualizado
        body_data = body.model_dump(exclude_none=True)
        body_data["updated_at"] = datetime.utcnow()  # ou timezone-aware se quiser

        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(f"Product not found with id: {id}")

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()
