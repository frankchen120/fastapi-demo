from fastapi import Depends
from app.core.exceptions import UnauthorizedError
from app.dependencies.auth import get_current_user
from app.models.enums import UserRole

def require_role(*roles: UserRole):
    def _checker(current_user = Depends(get_current_user)):
        if current_user.role not in roles:
            raise UnauthorizedError("insufficient permissions")
        return current_user
    return _checker
