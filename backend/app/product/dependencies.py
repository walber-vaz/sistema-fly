import os
from uuid import UUID

from fastapi import UploadFile
from PIL import Image

from app.config import settings


async def save_image(
    image: UploadFile, user_id: UUID, product_id: UUID, update_image: bool = False
) -> str:
    os.makedirs(f'static/images/products/{user_id}', exist_ok=True)

    try:
        filename = f'{product_id}.webp'
        image_path = f'static/images/products/{user_id}/{filename}'

        if os.path.exists(image_path) and not update_image:
            return f'{settings.BASE_URL_API}{image_path}'
        elif os.path.exists(image_path) and update_image:
            os.remove(image_path)

        with Image.open(image.file) as img:
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            img.save(image_path, 'WEBP')

        return f'{settings.BASE_URL_API}{image_path}'
    except Exception as e:
        if os.path.exists(image_path):
            os.remove(image_path)
        raise e
