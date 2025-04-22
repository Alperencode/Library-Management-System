from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from internal.models.admin import Admin, PublicAdmin
from internal.types.responses import PublicAdminResponse, FailResponse
from internal.types.types import AdminUpdateRequest, SUCCESS, FAIL, AdminRequest
from internal.database.admins import get_admin_by_id, update_admin, create_admin, get_admin_by_email
from internal.utils.utils import hash_password, get_current_admin

router = APIRouter(prefix="/admin")


@router.get("/me", response_model=PublicAdminResponse)
async def get_current_admin_info(admin: Admin = Depends(get_current_admin)):
    return PublicAdminResponse(
        code=SUCCESS,
        message="Admin details retrieved successfully",
        admin=PublicAdmin(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            role=admin.role
        )
    )


@router.patch("/me", response_model=PublicAdminResponse)
async def update_admin_info(update_data: AdminUpdateRequest, admin: Admin = Depends(get_current_admin)):
    admin = await get_admin_by_id(admin.id)
    if not admin:
        return JSONResponse(status_code=404, content=jsonable_encoder(
            FailResponse(
                code=FAIL,
                message="Admin not found"
            )
        ))

    is_updated = False
    if update_data.username and update_data.username != admin.username:
        admin.username = update_data.username
        is_updated = True
    if update_data.email and update_data.email != admin.email:
        admin.email = update_data.email
        is_updated = True
    if update_data.password and not admin.check_password(update_data.password):
        admin.password = hash_password(update_data.password)
        is_updated = True

    if is_updated:
        updated = await update_admin(admin)
        if not updated:
            return JSONResponse(status_code=500, content=jsonable_encoder(
                FailResponse(
                    code=FAIL,
                    message="Failed to update admin details"
                )
            ))

    return PublicAdminResponse(
        code=SUCCESS,
        message="Admin details updated successfully",
        admin=PublicAdmin(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            role=admin.role
        )
    )


@router.post("/register-admin", response_model=PublicAdminResponse)
async def register_admin(
    request_body: AdminRequest,
    request: Request,
    response: Response,
    admin: Admin = Depends(get_current_admin)
):
    existing_admin = await get_admin_by_email(request_body.email)
    if existing_admin:
        return JSONResponse(
            status_code=409,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Email already registered as admin"
            ))
        )

    admin = Admin(
        username=request_body.username,
        email=request_body.email,
        password=hash_password(request_body.password),
        role="admin"
    )

    created_admin = await create_admin(admin)
    if not created_admin:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(FailResponse(
                code=FAIL,
                message="Failed to create admin in database"
            ))
        )

    return PublicAdminResponse(
        code=SUCCESS,
        message="Admin registration successful",
        admin=PublicAdmin(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            role=admin.role
        )
    )
