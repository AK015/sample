# v1.0.0
import os
import errno
import datetime
from path import Path
from generic.arghelper import save_args_as_json
from logging import INFO, DEBUG, getLogger, StreamHandler, FileHandler, Formatter


class MYLogger(object):
    """
    Usage:
        01 : from mylogger import MYLogger
        02 : logger = MLLogger(module_name=__name__, file_name=__file__, init=True)
        03 : logger.my_logger.info("Test message")
        04 : save_dir = logger.get_savedir()

    NOTSET  :0
    DEBUG   :10
    INFO    :20
    WARNING :30
    ERROR   :40
    CRITICAL:50
    """
    def __new__(self, module_name=__name__, file_name=__file__, win_or_lin="lin",
                root_dir="./log", tmplog_name="latest_log.log", init=True, console_level=INFO, file_level=DEBUG, log_save=True):
        if not hasattr(self, "__instance__"):
            self.__instance__ = super(MYLogger, self).__new__(self)
            self.console_level = console_level
            self.file_level = file_level
            self.tmplog_name = tmplog_name
            self.my_logger = getLogger(module_name)
            self.root_dir = root_dir
            self.file_name = file_name
            self.win_or_lin = win_or_lin
            self.log_save = log_save

            if init:
                self.initialize(self.__instance__)
        return self.__instance__


    def initialize(self):
        date = datetime.datetime.now()
        self.my_logger.setLevel(self.file_level)

        self.dir_name = os.path.splitext(os.path.basename(self.file_name))[0]
        self.save_dir = os.path.join(self.root_dir, self.dir_name)

        # CONSOLE
        sh = StreamHandler()
        sh.setLevel(self.console_level)
        self.my_logger.addHandler(sh)


        if self.log_save:
            self.log_fn = os.path.join(self.save_dir, 'log_{}.log'.format(date.strftime('%y_%m_%d_%H%M%S')))
            Path(self.save_dir).makedirs_p()

            # FILE
            fh = FileHandler(self.log_fn, 'w', encoding='utf-8')
            fh.setFormatter(Formatter('%(asctime)s [%(levelname)-8s:%(levelno)s] (%(filename)s | %(funcName)s | line:%(lineno)04d) %(message)s'))
            fh.setLevel(self.file_level)
            self.my_logger.addHandler(fh)
            self.my_logger.propagete = False

            # Create symlink: if exists, remove old symlink
            if self.win_or_lin == "lin":
                try:
                    os.symlink(self.log_fn, self.tmplog_name)
                except OSError as e:
                    if e.errno == errno.EEXIST:
                        os.remove(self.tmplog_name)
                        os.symlink(self.log_fn, self.tmplog_name)


    def __str__(self):
        if self.log_save:
            return "log file is saved to \"" + self.log_fn + "\""
        else:
            return "log file isn't saved"


def log_dacorator(module_name=__name__, file_name=__file__, win_or_lin="lin",
                            root_dir="../log", tmplog_name="latest_log.log", init=True, console_level=INFO, file_level=DEBUG, log_save=True, comment=None):
    def _dacorator(main_fnc):
        def _wrapper():
            # === Preprocessing
            logger = MYLogger(module_name=module_name, file_name=file_name, win_or_lin=win_or_lin,
                                root_dir=root_dir, tmplog_name=tmplog_name, init=init, console_level=console_level, file_level=file_level, log_save=log_save)
            logger.my_logger.debug("COMMENT : \"{}\"".format(comment))
            logger.my_logger.info(logger)
            # ===
            args = main_fnc(logger)
            logger.my_logger.debug(vars(args))
            # === Post-processing
            if args.args_save:
                args_save_path = save_args_as_json(args, file_name)
                logger.my_logger.info(args_save_path)
            # ===
        return _wrapper
    return _dacorator

