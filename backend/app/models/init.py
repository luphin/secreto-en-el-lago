from .user import UserBase, UserCreate, UserUpdate, UserInDB, UserResponse
from .document import DocumentBase, DocumentCreate, DocumentUpdate, DocumentInDB, DocumentResponse
from .ejemplar import EjemplarBase, EjemplarCreate, EjemplarUpdate, EjemplarInDB, EjemplarResponse
from .loan import LoanBase, LoanCreate, LoanUpdate, LoanInDB, LoanResponse, LoanItem
from .request import RequestBase, RequestCreate, RequestUpdate, RequestInDB, RequestResponse, RequestItem

# Importar enums desde schemas
from app.schemas.user import UserRole, UserStatus
from app.schemas.document import DocumentType, DocumentCategory, MediaFormat, DocumentStatus
from app.schemas.ejemplar import EjemplarStatus
from app.schemas.loan import LoanType, LoanStatus
from app.schemas.request import RequestType, RequestStatus

__all__ = [
    # User
    "UserBase", "UserCreate", "UserUpdate", "UserInDB", "UserResponse", "UserRole", "UserStatus",
    
    # Document
    "DocumentBase", "DocumentCreate", "DocumentUpdate", "DocumentInDB", "DocumentResponse",
    "DocumentType", "DocumentCategory", "MediaFormat", "DocumentStatus",
    
    # Ejemplar
    "EjemplarBase", "EjemplarCreate", "EjemplarUpdate", "EjemplarInDB", "EjemplarResponse",
    "EjemplarStatus",
    
    # Loan
    "LoanBase", "LoanCreate", "LoanUpdate", "LoanInDB", "LoanResponse", "LoanItem",
    "LoanType", "LoanStatus",
    
    # Request
    "RequestBase", "RequestCreate", "RequestUpdate", "RequestInDB", "RequestResponse", "RequestItem",
    "RequestType", "RequestStatus",
]
