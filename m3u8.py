import requests
import os
import re
import zipfile
from tqdm import tqdm
import threading
from queue import Queue

def m3u8_video(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    respones = requests.get(url=url, headers=headers)
    respones.encoding = 'utf-8'
    m3u8_video = re.findall("video(.*?)';", respones.text)[0].replace('\'', '').split()[1]
    m3u8_host = re.findall("var m3u8_host(.*?)';", respones.text)[0].split('\'')[1]
    m3u8 = m3u8_host + m3u8_video
    # print(respones.text)
    file_path(respones, headers, m3u8_host, m3u8)


def file_path(respones, headers, m3u8_host, m3u8):
    title = re.findall('<a href="javascript:;">(.*?)</a>', respones.text)[1]
    filename = f'{title}\\'
    if not os.path.exists(filename):
        os.mkdir(filename)
    ts_download(headers, m3u8_host, filename, m3u8)


def ts_download(headers, m3u8_host, filename, m3u8):
    m3u8_data = requests.get(url=m3u8, headers=headers).text
    m3u8_data = re.sub('#EXTM3U', '', m3u8_data)
    m3u8_data = re.sub('#EXT-X-VERSION:\d', '', m3u8_data)
    m3u8_data = re.sub('#EXT-X-TARGETDURATION:\d+', '', m3u8_data)
    m3u8_data = re.sub('#EXT-X-MEDIA-SEQUENCE:\d+', '', m3u8_data)
    m3u8_data = re.sub('#EXTINF:\d+\.\d+,', '', m3u8_data)
    m3u8_data = re.sub('#EXT-X-ENDLIST', '', m3u8_data).split()
    for link in tqdm(m3u8_data):
        ts_url = m3u8_host + '/biantai/2019_01/18/biantai_HdXKPpQe_wm/' + link  # bug需要解决
        ts_name = link.split('m')[2]
        ts_content = requests.get(url=ts_url, headers=headers).content
        with open(filename + ts_name, mode='wb')as f:
            f.write(ts_content)
    print(m3u8_data)


# def ts_merge():
#     print("="*100)
#     print("开始合并")
#     files = os.listdir(filename)
#     with zipfile.ZipFile(filename+'.mp4', mode='w')as z:
#         for file in files:
#             path = filename + file
#             z.write(path)
#             # os.remove(path)
#             print(path)
#     print("合并完成")
if __name__ == '__main__':
    m3u8_video('https://www.ec23f.com/shipin/play-48269.html?road=1')
