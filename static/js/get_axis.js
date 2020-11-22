var axis_list = []
var out_end = []
flag = 0
function init()
{
    // クリック位置の座標取得
    document.onmousedown=function(){get_down_value();}
    // 画像のドラッグ & ドロップを禁止にする
    document.ondragstart = function(){return false;};
    // 画像の座標取得
    var elem = document.getElementById('target_image');
    var r = elem.getBoundingClientRect();

    // 画像の座標をセット
    document.getElementById("image_axis_x").value=r.left;
    document.getElementById("image_axis_y").value=r.top;
    document.getElementById("image_axis_width").value=r.width;
    document.getElementById("image_axis_height").value=r.height;
}

function get_down_value()
{
    var elem = document.getElementById('target_image');
    var r = elem.getBoundingClientRect();

    //イメージ画像の位置データ
    var image_x = r.left;
    var image_y = r.top;
    var image_width = r.width;
    var image_height = r.height;

    var annotation_x = 0;
    var annotation_y = 0;
    //クリック位置のx座標が画像のx座標より上側にあった場合
    if(event.x < image_x){
        annotation_x=0
    }
    //クリック位置のx軸が画像の範囲内にあった場合
    else if(event.x < image_x + image_width){
        annotation_x = event.x - image_x
    }

    else{
        annotation_x = image_width
    }

    //クリック位置のy座標が画像のy座標より上側にあった場合
    if(event.y < image_y){
        annotation_y=0
    }
    //クリック位置のy軸が画像の範囲内にあった場合
    else if(event.y < image_y + image_height){
        annotation_y = event.y - image_y
    }
    else{
        annotation_y = image_height
    }
    if(flag % 2 == 0){
    axis_list = []
    axis_list.push([annotation_x, annotation_y])
    }
    else if(flag % 2 == 1){
    axis_list.push([annotation_x, annotation_y])
    document.getElementById("axis_list").value = axis_list
    }
    flag = flag + 1
    document.getElementById("tx1").value = annotation_x
    document.getElementById("ty1").value = annotation_y
}
