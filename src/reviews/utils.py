def get_path_upload_image(instance, file):
    """Построение пути к фото."""

    return f'uploads/user_{instance.user.id}/%Y/%m/%d/{file}'
