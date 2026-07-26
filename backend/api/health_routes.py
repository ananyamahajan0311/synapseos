from fastapi import APIRouter

router = APIRouter(tags=["Health"])

@router.get("/")
def root():
    return {"message": "SynapseOS Backend Running"}

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SynapseOS Backend"
    }