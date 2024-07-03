# v1.0.0
COMMENT = "画像から正方形を切り抜いて画像上にファイル名をプロットするプログラム" # なぜ実行したのかなど，logファイルの1行目に記録できる
import os
import csv
import datetime
from logging import INFO, DEBUG
from generic.mylogger import log_dacorator
from generic.myfunction import get_args_for_010, make_output_dir, main_processing


@log_dacorator(module_name=__name__, file_name=__file__, init=True,
                            console_level=INFO,
                            log_save=True,
                            comment = COMMENT)
def main(logger):
    args = get_args_for_010()

    ##########################
    input_dir = args.input_dir
    output_dir = args.output_dir
    test_run = args.test_run

    ##########################
    dt = datetime.datetime.now()
    dt_txt = dt.strftime('%Y_%m_%d_%H%M%S') if not test_run else "test_" + dt.strftime('%Y_%m_%d_%H%M%S')

    ##########################
    csv_file = open(os.path.join(input_dir, "list.csv")) if not test_run else open(os.path.join(input_dir, "list_test.csv"))
    csv_data = csv.reader(csv_file) #TODO

    for row in csv_data:
        logger.my_logger.info("input_dir_name : {}".format(row[0]))

        input_dir_fullname = os.path.join(input_dir, row[0])
        logger.my_logger.debug("input_dir_fullname : {}".format(input_dir_fullname))

        output_dir_fullname = make_output_dir(logger, output_dir, __file__, dt_txt, input_dir_fullname, dir_name=None)
        input_img_list = os.listdir(input_dir_fullname)
        logger.my_logger.info("input_img_list : {}".format(input_img_list))

        for input_img in input_img_list:
            logger.my_logger.info("input_img : {}".format(input_img))
    
            input_img_path = os.path.join(input_dir_fullname, input_img)
            logger.my_logger.debug("input_img_path : {}".format(input_img_path))

            output_img_path = os.path.join(output_dir_fullname, input_img)
            logger.my_logger.debug("output_img_path : {}".format(output_img_path))

            main_processing(logger, input_img_path, output_img_path)
    ##########################

    return args


if __name__ == '__main__':
    main()

