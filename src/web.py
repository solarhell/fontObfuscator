import uuid

from sanic import Sanic
from sanic.response import json, text

from config import BUCKET_HOST
from src.core import obfuscate, obfuscate_plus
from src.model import common_response
from src.upload import upload_to_oss, delete_file
from src.utils import base64_binary

app = Sanic()


@app.get('/')
async def index(request):
    return text('it works')


@app.post('/api/encrypt')
async def encrypt(request):
    # print(request.json)
    plain_text = request.json['plaintext']
    shadow_text = request.json['shadowtext']
    only_ttf = request.json['only_ttf']
    upload = request.json['upload']
    try:
        filename = str(uuid.uuid4())
        font_files = obfuscate(plain_text, shadow_text, filename, only_ttf, 'output')

        base64ed = {}
        if upload:
            oss_file_path = {}

        for format, filepath in font_files.items():
            base64ed[format] = base64_binary(filepath)

            if upload:
                upload_to_oss(f'{filename}.{format}', filepath)
                oss_file_path[format] = f'{BUCKET_HOST}/{filename}.{format}'

            delete_file(filepath)

        resp = {'base64ed': base64ed}
        if upload:
            resp['files'] = oss_file_path

        return json(common_response(success=True, data=resp))
    except Exception as e:
        return json(common_response(success=False, data=None, hint=str(e)))


@app.post('/api/encrypt-plus')
async def encrypt(request):
    # print(request.json)
    plain_text = request.json['plaintext']
    only_ttf = request.json['only_ttf']
    upload = request.json['upload']
    try:
        filename = str(uuid.uuid4())
        font_files, html_entities = obfuscate_plus(plain_text, filename, only_ttf, 'output')

        base64ed = {}
        if upload:
            oss_file_path = {}

        for format, filepath in font_files.items():
            base64ed[format] = base64_binary(filepath)

            if upload:
                upload_to_oss(f'{filename}.{format}', filepath)
                oss_file_path[format] = f'{BUCKET_HOST}/{filename}.{format}'

            delete_file(filepath)

        resp = {'base64ed': base64ed,
                'html_entities': html_entities, }
        if upload:
            resp['files'] = oss_file_path

        return json(common_response(success=True, data=resp))
    except Exception as e:
        return json(common_response(success=False, data=None, hint=str(e)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1323, debug=False)
