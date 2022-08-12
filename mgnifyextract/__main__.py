import logging


logging_level = logging.DEBUG
logging_fmt = "%(asctime)s - %(levelname)5.5s - %(name)10.10s - %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging_level, format=logging_fmt, datefmt=date_fmt)


if __name__ == "__main__":

    # parser = argparse.ArgumentParser()
    # parser.add_argument("-d", "--datadir", help="data directory", dest="data_dir", default="./data")
    # parser.add_argument("-p", "--pipeline", help="pipeline version", dest="pipeline", default="4.1")
    # args = parser.parse_args()
    # run(abspath(args.data_dir), args.pipeline)

    pass
