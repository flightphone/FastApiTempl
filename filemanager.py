from fastapi import Depends, UploadFile, File, Request
import os
from dependencies import get_api_current_user, get_engine, get_current_user
from setting import gethtml


from fastapi import APIRouter
router = APIRouter()


@router.get("/user")
async def userinfo(request:Request, current_user = Depends(get_current_user)):
    return gethtml("user.html", {"request": request})

@router.get("/files")
async def files_info(request:Request, current_user = Depends(get_current_user)):
    return gethtml("files.html", {"request": request})

@router.post("/uploadfiles")
async def create_upload_files(files: list[UploadFile]= File(description="Multiple files as UploadFile"), current_user = Depends(get_api_current_user)):
    if not files:
        return {"message": "No file sent"}
    filepath = f"userfiles\\user{current_user['id']}"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    for f in files:
        fname = f"{filepath}/{f.filename}"
        with open(fname, "wb") as sf:
            content = f.file.read()
            sf.write(content)
    return {"filenames": [file.filename for file in files]}

@router.post("/files_data")    
async def files(current_user = Depends(get_api_current_user)):
    filepath = f"userfiles\\user{current_user['id']}"
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    return os.listdir(filepath)

   
