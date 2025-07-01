from http import HTTPStatus
from app.core.settings import settings
from http import HTTPStatus
from uuid import UUID
import httpx
from app.exceptions import UserNotFoundException

class CustomerClient(): 
    async def fetch_user(self, customer_id: UUID):
        JWT_TOKEN = settings.CUSTOMER_API_KEY
        async with httpx.AsyncClient() as client:   
            headers={
                "Authorization": f"Bearer {JWT_TOKEN}",
                "Content-Type": "application/json"
            }
            response = await client.get(settings.CUSTOMER_API + f"/customer/{customer_id}", headers=headers)
            if(response.status_code == HTTPStatus.NOT_FOUND):
                raise UserNotFoundException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
            return response.json()