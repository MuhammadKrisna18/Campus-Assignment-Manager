from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()


def require_role(
    allowed_roles: list
):

    def role_checker(
        credentials=Depends(security)
    ):

        # nanti decode JWT

        return credentials

    return role_checker