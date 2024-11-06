import os
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from app.domain.models.file_model import FileModel


class FileUploadHelper:
    def __init__(self, db: Session, upload_dir: str = "static",
                 allowed_extensions: set = None):
        self.upload_dir = upload_dir
        self.allowed_extensions = allowed_extensions or {'png', 'jpg', 'jpeg', 'pdf', 'docx'}
        self.db = db
        os.makedirs(self.upload_dir, exist_ok=True)

    def allowed_file(self, filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    async def save_file(self, file: UploadFile) -> FileModel:
        """
        Сохраняет файл в указанную директорию, если его расширение разрешено,
        и создает запись в базе данных с информацией о файле.

        :param file: Файл для загрузки.
        :return: Экземпляр FileModel с информацией о файле.
        :raises ValueError: Если расширение файла не разрешено.
        """
        # Проверка и безопасное имя файла
        filename = secure_filename(file.filename)
        if not self.allowed_file(filename):
            raise ValueError(f"Недопустимое расширение файла: {filename}")

        # Полный путь к файлу
        file_path = os.path.join(self.upload_dir, filename)

        # Сохранение файла на сервере
        with open(file_path, "wb") as f:
            content = await file.read()  # Чтение содержимого файла
            f.write(content)  # Запись в файл

        # Создание записи в базе данных
        file_record = FileModel(
            url=file_path,
            extension=filename.rsplit('.', 1)[1].lower(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        self.db.add(file_record)
        await self.db.commit()
        await self.db.refresh(file_record)

        return file_record
