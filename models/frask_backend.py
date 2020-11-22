from flask import request
import os
import sys
import cv2

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
        self.target_index_number = -1

        self.box_list = []

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
        if request.form.get('add_box_data') is None:
            self.target_index_number += 1
        return self.target_index_number

    def reset_index_number(self):
        self.target_index_number = -1
        return 0

    def catch_axis_data_for_draw_boxes(self):
        square_coordinates_str = request.form.get('axis_data_for_draw_boxes')
        if square_coordinates_str is not None:
            square_coordinates_str = square_coordinates_str.split(',')
            x1 = int(square_coordinates_str[0])
            y1 = int(square_coordinates_str[1])
            x2 = int(square_coordinates_str[2])
            y2 = int(square_coordinates_str[3])
            self.box_list.append([x1, y1, x2, y2])
            return self.box_list
        else:
            return 0


class Process_Image(object):
    def __init__(self, box_list, image_path):
        self.box_list = box_list
        self.image = cv2.imread(image_path)

    def draw_boxes(self):
        image2 = self.image.copy()
        for i in self.box_list:
            x1 = i[0]
            y1 = i[1]
            x2 = i[2]
            y2 = i[3]
            image2 = cv2.rectangle(self.image, (x1, y1), (x2, y2),
                                   (255, 255, 0), 3)
        ret, jpeg = cv2.imencode('.jpg', image2)
        return jpeg.tobytes()
