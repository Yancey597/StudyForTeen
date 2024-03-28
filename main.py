import zipfile
import os
from PIL import Image, ImageDraw, ImageFont
import requests
import requests.utils
from bs4 import BeautifulSoup

import random


def show_exit(content):
    """
    输出错误原因，辅助退出
    """
    input(content)
    exit()


def get_openid():
    count = 0;
    st = "oADCC6"  # 设定前缀
    s = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
         'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
         'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5',
         '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
         'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
         'x', 'y', 'z'];  # 'a','b','c','d','e','f','g','h','c'
    while (count < 22):
        i = random.randint(0, len(s))
        if (i >= 0 and i < len(s)):
            st += s[i];
            count += 1;
    return st


def get_image(s, code, course):
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = 'https://h5.cyol.com/special/daxuexi/' + code + '/images/end.jpg'
    resp = s.get(url, headers=headers)
    img_path = '1' + '.jpg'
    f = 0;
    with open(img_path, 'wb') as fp:
        fp.write(resp.content)
        f = 1
    if (f == 1):
        print("图片获取成功")
    else:
        print("图片获取失败")


def get_code(s):
    """
    调用API获取最新一期青春学习的CODE
    :return:
    """
    url = "https://h5.cyol.com/special/weixin/sign.json"
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Origin": "http://h5.cyol.com",
        "X-Requested-With": "com.tencent.mm",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    resp = s.get(url, headers=headers).json()
    return list(resp)[-1]


def get_course(s, code):
    headers = {
        "Host": "h5.cyol.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/tpg,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = 'https://h5.cyol.com/special/daxuexi/' + code + '/m.html'
    resp = s.get(url, headers=headers)
    soup = BeautifulSoup(resp.content.decode("utf8"), "lxml")
    course = soup.title.string[7:]
    return course


def save_door(course, s, school, name, clas, dept):
    """
    调用API提交用户进入页面信息至青春湖北数据库
    :param info:
    :return:
    """
    headers = {
        "Host": "cp.fjg360.cn",
        "Connection": "keep-alive",
        "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; PACM00 Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3164 MMWEBSDK/20211001 Mobile Safari/537.36 MMWEBID/556 MicroMessenger/8.0.16.2040(0x28001056) Process/toolsmp WeChat/arm32 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    url = "https://cp.fjg360.cn/index.php?m=vote&c=index&a=save_door&sessionId=&imgTextId=&ip="
    # url += get_ip()
    url += "&username=" + name
    url += "&phone=" + "未知"
    url += "&city=" + school  # info["danwei1"]
    url += "&danwei2=" + clas  # info["danwei3"]
    url += "&danwei=" + dept  # info["danwei2"]
    url += "&openid=" + get_openid()  # 随机的openid
    url += "&num=10"
    url += "&lesson_name=" + course  # 大学习第几期
    resp = s.get(url, headers=headers).json()
    if resp.get("code") == 1:
        print("%s %s %s True" % (name, clas, dept))
        return True
    else:
        show_exit("您的用户信息有误，请检查后重试")

def add_watermark(input_path, output_path):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    watermark_text = os.path.splitext(os.path.basename(input_path))[0]  # 获取文件名（不带扩展名）
    font = ImageFont.truetype('msyh.ttc', 100)
    text_width, text_height = draw.textsize(watermark_text, font)
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    draw.text((x, y), watermark_text, fill=(255, 255, 255), font=font)
    image.save(output_path)
    image.close()

def rename_image(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"图片 {old_name} 重命名为 {new_name}")
    except FileNotFoundError:
        print(f"图片 {old_name} 不存在或无法重命名")

def zip_images(directory, zip_filename):
    # 创建一个压缩文件并将目录中的所有图像添加到其中
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)

def run():
    names = [

    ]
    s = requests.session()
    code = get_code(s)
    course = get_course(s, code)

    school =''
    clas = ''
    dept = ''
    for name in names:
        save_door(course, s, school, name, clas, dept)
        get_image(s, code, course)

        old_name = '1.jpg'  # 假设图片名字为 '1.jpg'
        new_name = f'{name}.jpg'
        rename_image(old_name, new_name)
        add_watermark(new_name, new_name)

    # 创建一个目录来保存图片
    output_directory = 'output_images'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 将带有水印的图片放入一个目录
    for name in names:
        os.rename(f'{name}.jpg', f'{output_directory}/{name}.jpg')

    # 压缩目录中的图片
    zip_images(output_directory, 'images.zip')


def show():
    print("如果您\n同意:请输入 yes 运行本程序\n不同意:输入 no 关闭本程序")


if __name__ == '__main__':
    show()
    run()
    show_exit("运行完成")