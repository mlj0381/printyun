# 自定义函数

import PyPDF2, subprocess, os, filetype, uuid, datetime, hashlib, json, requests, redis
from app.models import User


# from rq import Queue
# from app.worker import conn

# q = Queue(connection=conn)

# pool = redis.ConnectionPool(host='192.168.1.199', port=6379, password='Zxs123456', decode_responses=True)
# redis_client = redis.Redis(connection_pool=pool)



# 定义文件转换后保存的目录
basepath = os.path.abspath(os.path.dirname(__file__))
FileSaveDir = os.path.join(basepath, 'static/Upload_Files')



# 读取pdf页数
# def read_pdf_pages(file):
#     with open(file, 'rb') as PdfFileObj:
#         try:
#             PdfReader = PyPDF2.PdfFileReader(PdfFileObj)
#         except:
#             return None
#         else:
#             return PdfReader.numPages

def read_pdf_pages(file):
    with open(file, 'rb') as PdfFileObj:
        PdfReader = PyPDF2.PdfFileReader(PdfFileObj)
        return PdfReader.numPages


# 转pdf
def switch_topdf(filename):
    # cmd = "libreoffice --headless --convert-to pdf:writer_pdf_Export {} --outdir {}".format(filename, FileSaveDir) #mac linux

    cmd = "soffice --headless --convert-to pdf:writer_pdf_Export {} --outdir {}".format(filename, FileSaveDir)  # win
    print(cmd)
    try:
        returnCode = subprocess.call(cmd, shell=True)
        # returnCode = os.system(cmd)
        if returnCode != 0:
            raise IOError("{} failed to switch".format(filename))
    except Exception:
        return 1
    else:
        return 0


# 随机取文件名
def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# 判断日期并记录数字
def date_count(db_date):
    if db_date.Born_Date_Day == datetime.datetime.now().date():
        macs = int(db_date.Trade_Number[9:]) + 1
        return macs
    else:
        macs = 1
        return macs


def sign(*p):
    return hashlib.md5(u''.join(p).encode('utf8')).hexdigest().lower()


def query_status(aoid):
    resp = requests.get('https://xorpay.com/api/query/' + aoid)
    return json.loads(resp.text)


def bedict_order(items):
    lic = []
    for item in items:
        tel = User.query.order_by(User.Id == item.User_Id)
        dicts = {
            'Print_Money': item.Print_Money,
            'File_Name': item.File_Name,
            'Print_Status': item.Print_Status,
            'Print_Copies': item.Print_Copies,
            'Print_Colour': item.Print_Colour,
            'Print_size': item.Print_size,
            'Print_way': item.Print_way,
            'Print_Direction':item.Print_Direction,
            'Trade_Number': item.Trade_Number,
            'tel_num': tel
            }
        lic.append(dicts)
    return lic


def bedict_order_date(items , b):
    da = datetime.datetime.strptime(b, '%Y-%m-%d').date()
    lic = []
    for item in items:
        if da == item.Born_Date_Day:
            born_date = str(item.Born_Date.year) + "-" + str(item.Born_Date.month) + "-" + str(
                item.Born_Date.day) + " " + str(item.Born_Date.hour) + ":" + str(item.Born_Date.minute) + ":" + str(
                item.Born_Date.second)
            lic.append(
                {
                'Print_Money': item.Print_Money,
                'File_Name': item.File_Name,
                'Born_Date': born_date,
                'Print_Place': item.Print_Place,
                'Print_Status': item.Print_Status,

                'Print_Copies': item.Print_Copies,
                'Print_Colour': item.Print_Colour,
                'Print_size': item.Print_size,
                'Print_way': item.Print_way,
                'Print_Direction':item.Print_Direction,
                'Print_Date': item.Print_Date,
                'File_Dir': item.File_Dir,
                'Trade_Number': item.Trade_Number
                }
            )
    return lic