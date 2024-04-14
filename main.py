from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的来源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的方法
    allow_headers=["*"],  # 允许的头部
)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"files/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())
        return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/preview/")
async def preview_files():
    files_directory = "files/"
    files_list = []
    for filename in os.listdir(files_directory):
        if os.path.isfile(os.path.join(files_directory, filename)):
            files_list.append(filename)
    return {"files": files_list}


@app.delete("/delete/{file_name}")
async def delete_file(file_name: str):
    file_location = f"files/{file_name}"
    if os.path.exists(file_location):
        try:
            os.remove(file_location)
            return {"info": f"File '{file_name}' successfully deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail=f"File '{file_name}' not found")


@app.get("/download/{file_name}")
async def download_file(file_name: str):
    file_location = f"files/{file_name}"
    if os.path.exists(file_location):
        return FileResponse(
            file_location, media_type="application/pdf", filename=file_name
        )
    raise HTTPException(status_code=404, detail=f"File {file_name} not found")
