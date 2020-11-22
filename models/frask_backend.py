from flask import request
import os
import sys

sys.dont_write_bytecode = True

# 保存できるファイルの拡張子
ALLOWED_EXTENSION_NAMES = {'png', 'jpg'}


def allowed_extensions(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION_NAMES


class Flask_Event(object):
    def __init__(self):
        # データセットを作成したいモデル名
        self.ml_model_name = None
        # アノテーション画像のインデックス番号
        self.target_index_number = 0

    @staticmethod
    def upload_files(upload_folder):
        files = request.files.getlist('files')
        for file in files:
            if file and allowed_extensions(file.filename):
                file_name = file.filename
                file.save(os.path.join(upload_folder, file_name))
        return 0

    def catch_ml_model_name(self):
        self.ml_model_name = request.form.get('deep_learning_model')

    def catch_target_index(self):
        self.target_index_number += 1
        return self.target_index_number

    def reset_index_number(self):
        self.target_index_number = 0
        return 0
