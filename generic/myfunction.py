# v1.0.0
import os
import argparse
from path import Path
from PIL import Image, ImageDraw, ImageFont
from generic.arghelper import LoadFromJson


###!  よく使う関数 ####
# === 出力先ディレクトリを作成する関数
def make_output_dir(logger, output_dir, filepath, dt_txt, input_dir, dir_name=None):
    tmp_input_dir_name = os.path.basename(input_dir)
    tmp_output_dir_name = os.path.join(output_dir, os.path.splitext(os.path.basename(filepath))[0])
    tmp_output_dir_name = os.path.join(tmp_output_dir_name, dt_txt)

    output_dir_name = os.path.join(tmp_output_dir_name, tmp_input_dir_name)
    if not dir_name==None:
        output_dir_name = os.path.join(output_dir_name, dir_name)
    if not os.path.isdir(output_dir_name):
        Path(output_dir_name).makedirs_p()
        logger.my_logger.info("make directory : \"{}\"".format(output_dir_name))
    return output_dir_name


###!  010_test.py用の関数 ####
# === コマンドライン引数
def get_args_for_010():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--input_dir', type=str, default=None, required=True, help='Select input directory.')
    parser.add_argument('--output_dir', type=str, default=None, required=True, help='Select output directory.')
    parser.add_argument('--test_run', action="store_true", default=False, help='test')
    parser.add_argument('--args_save', action="store_true", default=False, help='Save args as a json file.')
    parser.add_argument('--cond', type=str, action=LoadFromJson)
    return parser.parse_args()


# === 画像から正方形を切り抜いて画像上にファイル名をプロットする関数
def main_processing(logger, input_img_path, output_img_path):
    file_name = os.path.splitext(os.path.basename(input_img_path))[0]
    logger.my_logger.debug("filename : " + file_name)
    in_img = Image.open(input_img_path).convert("RGB")
    tmp_img = crop_max_square(in_img)
    out_img = write_letters(tmp_img, " filename : " + file_name)
    out_img.save(output_img_path, quality=95)


# === トリミング用関数
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


# === 画像から正方形を切り抜く関数
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


# === 画像へ文字を書き込む関数
def write_letters(pil_img, text, font_size=40):
    # font_path = 'C:\Windows\Fonts\meiryo.ttc'   #   Windowsのフォントファイルへのパス
    font_path = './generic/sunnyday/fontopoSunnyDay-Regular.otf'
    drawer = ImageDraw.Draw(pil_img)
    font = ImageFont.truetype(font_path, font_size)
    drawer.text(xy=(0, 0), text=text, font=font, fill=(255, 0, 0))
    return pil_img

