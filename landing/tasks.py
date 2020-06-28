import os
from pathlib import Path
from typing import List
from zipfile import ZipFile
from PIL import Image
from django.conf import settings
from TestTask.celery_app import app

import logging
logger = logging.getLogger('task_image_resizer')


# resize image to current width and current height
@app.task(name="image")
def resize_image(file_paths: List[Path], w: int, h: int, name: str):
    logger.debug('started task image')
    zip_file = f"{name}.zip"
    with ZipFile(settings.MEDIA_ROOT+'/images/'+zip_file, "w") as zipper:
        results = {"archive_path": f"{settings.MEDIA_URL}images/{zip_file}"}
        for file_path in file_paths:
            file_path = Path(file_path)
            file_name = file_path.stem
            ext = file_path.suffix
            logger.debug("try %s", file_path.name)
            try:
                img = Image.open(file_path)
                file_path.unlink()
                img_copy = img.resize((w, h), Image.ANTIALIAS)
                thumbnail_file = f"{file_name}_{w}x{h}{ext}"
                img_copy.save(thumbnail_file)
                zipper.write(thumbnail_file)
                os.remove(thumbnail_file)
                img.close()
                logger.debug('file %s has resized', file_path.name)
            except IOError as e:
                logger.error(e)
    return results
