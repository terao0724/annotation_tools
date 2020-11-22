import os
import glob
import tempfile

from flask import Flask, render_template, request, redirect, url_for, Response

from models.frask_backend import Flask_Event, Process_Image

app = Flask(__name__)
flask_event = Flask_Event()

# 画像を保存するパス
UPLOAD_FOLDER = './static/uploads/'
ERROR_MESSAGES = {"upload_error": ["ファイルをアップロードできませんでした。",
                                   "[保存可能ファイル拡張子: 'jpg', 'png']"]}

app.config['SECRET_KEY'] = os.urandom(24)


def catch_files_list(upload_dir):
    uploaded_files_list = glob.glob(upload_dir + "*")
    return uploaded_files_list


def generate(camera):
    while True:
        frame = camera.draw_boxes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n'
               + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        flask_event.upload_files(UPLOAD_FOLDER)
        upload_file_names = catch_files_list(UPLOAD_FOLDER)

        if len(upload_file_names) != 0:
            return render_template('choose_deep_leaning_model.html')
        else:
            error_message = ERROR_MESSAGES["upload_error"]
            return render_template('upload.html',
                                   error_message=error_message)
    else:
        return redirect(url_for('index'))


@app.route('/save_model_name', methods=['GET', 'POST'])
def save_model_name():
    flask_event.catch_ml_model_name()
    return redirect('/create_metadata')


@app.route('/create_metadata', methods=['GET', 'POST'])
def create_metadata():
    file_index = flask_event.catch_target_index()
    upload_file_names = catch_files_list(UPLOAD_FOLDER)
    flask_event.catch_axis_data_for_draw_boxes()
    img_url = upload_file_names[file_index]
    return render_template('catch_metadata.html', img_url=img_url)


@app.route('/video_feed')
def video_feed():
    file_index = flask_event.target_index_number
    if file_index < 0:
        file_index = 0
    upload_file_names = catch_files_list(UPLOAD_FOLDER)
    print("AAAAAAAAAAAAAAAAA")
    image_path = upload_file_names[file_index]
    return Response(generate(Process_Image(flask_event.box_list.copy(), image_path)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


"""
@app.route('/save_metadata_to_local', methods=['GET', 'POST'])
def create_metadata():
"""

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000,
                        type=int, help="port to listen on")
    args = parser.parse_args()
    port = args.port
    app.config["port"] = port
    app.run(host="0.0.0.0", port=port, threaded=True, debug=True)
