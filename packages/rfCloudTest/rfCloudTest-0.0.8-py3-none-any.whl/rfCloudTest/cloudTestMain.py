import getopt
import sys
from builtins import print, Exception

from rfCloudTest.business import robotFileUtils


def help():
    msg = "*" * 100 + "\n" \
          + "您正在使用接口测试服务，请仔细查看使用说明\n" \
          + "--help or -h :显示帮助信息\n" \
          + "--file or -f : 指定命令执行的文件路径\n" \
          + "--env or -e : 指定运行的被测环境\n" \
          + "*" * 100
    print(msg)

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"-hf:e:",["help","file=","env="])
    except Exception:
        print('参数输入错误，请查看帮助文档')
        help()
        sys.exit(-1)
    options = []
    for opt,value in opts:
        options.append(opt)
    if ('-h' in options) or ('--help' in options):
        help()
        sys.exit(0)
    else:
        for opt,value in opts:
            if opt == '-f' or opt == '--file':
                FILE_PATH = value
        robotFileUtils.generate_robot_file_by_file_path(FILE_PATH)
        print('args='%args)
        robotFileUtils.run_case(args)
        sys.exit(0)
main()