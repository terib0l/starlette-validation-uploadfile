import os
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_Uploaded_File_Goes_Through():
    """
    Would upload file to "upload_file_first"
    Upload File is jpeg, and size less than 12000 bytes
    """
    size = os.path.getsize("./img/proper.jpeg")

    with open("./img/proper.jpeg", "rb") as img:
        response = client.post(
                "/upload/first",
                files={"file": ("proper.jpeg", img, "image/jpeg")}
                )

    assert response.status_code == 200
    assert response.json() == {
            "filename": "test.jpeg",
            "content_type": "image/jpeg",
            "file_size": size
            }

def test_Uploaded_File_Is_Too_Large_Size():
    """
    Would upload file to "upload_file_first"
    Upload File is jpeg, and size more than 12000 bytes
    """
    with open("./img/too_large.jpeg", "rb") as img:
        response = client.post(
                "/upload/first",
                files={"file": ("too_large.jpeg", img, "image/jpeg")}
                )

    assert response.status_code == 413
    assert response.json() == "Request Entity Too Large"

def test_Uploaded_File_Is_Unsupported_File_Type():
    """
    Would upload file to "upload_file_first"
    Upload File is png, and size less than 12000 bytes
    """
    with open("./img/unsupported_type.png", "rb") as img:
        response = client.post(
                "/upload/first",
                files={"file": ("unsupported_type.png", img, "image/png")}
                )
    response = client.post("/upload/first")
    assert response.status_code == 415
    assert response.json() == "Unsupported Media Type"

def test_When_No_Specified_In_App_Path_Uploaded_File_Goes_Through_Even_In_The_Case_Of_Too_Large_Size():
    """
    Would upload file to "upload_file_second"
    Upload File is jpeg, and size more than 12000 bytes
    """
    size = os.path.getsize("./img/too_large.jpeg")

    with open("./img/too_large.jpeg", "rb") as img:
        response = client.post(
                "/upload/second",
                files={"file": ("too_large.jpeg", img, "image/jpeg")}
                )
    assert response.status_code == 200
    assert response.json() == {
            "filename": "test.jpeg",
            "content_type": "image/jpeg",
            "file_size": size
            }

def test_When_No_Specified_In_App_Path_Uploaded_File_Goes_Through_Even_In_The_Case_Of_Unsupported_File_Type():
    """
    Would upload file to "upload_file_second"
    Upload File is png, and size less than 12000 bytes
    """
    size = os.path.getsize("./img/unsupported_type.png")

    with open("./img/unsupported_type.png", "rb") as img:
        size = 
        response = client.post(
                "/upload/second",
                files={"file": ("unsupported_type.png", img, "image/png")}
                )
    assert response.status_code == 200
    assert response.json() == {
            "filename": "test.jpeg",
            "content_type": "image/png",
            "file_size": size
            }
