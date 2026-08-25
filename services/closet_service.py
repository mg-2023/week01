import boto3
import uuid
from config import Config
from db import items


def upload_image_to_s3(file):
    s3 = boto3.client('s3',  
                      aws_access_key_id=Config.AWS_ACCESS_KEY, 
                      aws_secret_access_key=Config.AWS_SECRET_KEY,
                      region_name=Config.AWS_REGION
                      )

    filename = f"clothes/{uuid.uuid4().hex}_{file.filename}"

    s3.upload_fileobj(
        file,
        Config.S3_BUCKET_NAME, 
        filename, 
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"https://{Config.S3_BUCKET_NAME}.s3.{Config.AWS_REGION}.amazonaws.com/{filename}"


def create_closet_item(user_id, form_data, file):

    image_url = upload_image_to_s3(file)

    #DB 저장
    item_doc = {
        "user_id": user_id,
        "image_url": image_url,
        "brand": form_data.get("brand"),
        "buy_date": form_data.get("date"),
        "buy_method": form_data.get("method"),
        "price": int(form_data.get("price")) if form_data.get("price") else 0,
        "season": form_data.get("season"),
        "type": form_data.get("type"),
        "size": form_data.get("size")
    }

    result = items.insert_one(item_doc)
    return str(result.inserted_id)