import os
import django
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name='dtswouvsm',
    api_key='732922992783139',
    api_secret='qo9LHP4BkfAJiLHBuHermRI--gg'
)

MEDIA_ROOT = 'media'

for root, dirs, files in os.walk(MEDIA_ROOT):
    for filename in files:
        if filename == '.gitkeep':
            continue
        
        local_path = os.path.join(root, filename)
        public_id = os.path.splitext(local_path)[0]
        
        print(f'Загружаю {local_path}...')
        try:
            cloudinary.uploader.upload(
                local_path,
                public_id=public_id,
                overwrite=True,
                use_filename=True,
            )
            print(f'✓ {local_path}')
        except Exception as e:
            print(f'✗ Ошибка {local_path}: {e}')

print('Готово!')