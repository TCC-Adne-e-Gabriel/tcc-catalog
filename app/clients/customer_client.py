from http import HTTPStatus
from app.core.settings import settings
from http import HTTPStatus
from uuid import UUID
import httpx
from app.exceptions import UserNotFoundException

class CustomerClient(): 
    async def fetch_user(self, customer_id: UUID):
        return {
            "name": "adnew",
            "email": "um",
            "phone": "61995378511",
            "id": "8c02dec7-2ca4-4bd8-be7b-1e57a249802a",
            "created_at": "2025-06-30T15:04:17.670795",
            "updated_at": "2025-06-30T15:04:17.670807"
        }
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