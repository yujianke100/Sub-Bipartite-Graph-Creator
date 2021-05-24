# -*- coding: utf-8 -*-
from requests_html import HTMLSession
from time import time
from requests import get
from utils.os_control import *

s_path = './output/datas_tar/'
t_path = './output/datas_origin/'

# 爬虫获取数据集
def get_datasets(ui):
    url = 'http://konect.cc/networks/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.76'}

    session = HTMLSession()
    ui.change_init_status('Preparing crawler...')
    r = session.get(url=url, headers=headers)
    r.html.render()
    ui.change_init_status('Reading datasets\' names...')
    data_name = r.html.xpath(
        "//div[@id='page']/table[1]/tbody[1]/tr/td[2]")[1:]
    node_num = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[4]")[1:]
    edge_num = r.html.xpath("//div[@id='page']//table/tbody[1]/tr/td[5]")[1:]
    ui.change_init_status('Reading datasets\' availability...')
    avaliable_img = r.html.xpath(
        "//div[@id='page']//table/tbody[1]/tr/td[3]/img[1]")
    ui.change_init_status('Reading datasets\' verifiability...')
    test_img = r.html.xpath(
        "//div[@id='page']//table/tbody[1]/tr/td[3]/img[2]")
    ui.change_init_status('Reading datasets\' type 1...')
    first_data_types_img = r.html.xpath(
        "//div[@id='page']//table/tbody[1]/tr/td[3]/img[3]")
    ui.change_init_status('Reading datasets\' type 2...')
    second_data_types_img = r.html.xpath(
        "//div[@id='page']//table/tbody[1]/tr/td[3]/img[4]")

    #选取符合我们需求的数据集
    data_len = len(avaliable_img)
    data_list = []
    for i in range(data_len):
        if(avaliable_img[i].attrs['title'] == 'Dataset is available for download' and
           first_data_types_img[i].attrs['title'] == 'Bipartite, undirected' and
           second_data_types_img[i].attrs['title'] == 'Unweighted, multiple edges' and
           test_img[i].attrs['title'] == 'Dataset passed all tests'):
            try:
                timestamp = r.html.xpath(
                    "//div[@id='page']//table/tbody[1]/tr[{}]/td[3]/img[5]".format(i+2))[0].attrs['title']
                if(timestamp == 'Edges are annotated with timestamps'):
                    data_sname = list(data_name[i].links)[0][:-1]
                    data_list.append(
                        [i, data_name[i].text, node_num[i].text, edge_num[i].text, data_sname])
            except:
                pass
        ui.change_init_status(
            'Screening of graph...({}/{})'.format(i, data_len))
    return data_list

# https://blog.csdn.net/dqy74568392/article/details/96479370


# 下载文件并显示网速和下载进度
def downloader(data):
    if(not exists(s_path)):
        makedirs(s_path)
    if(not exists(t_path)):
        makedirs(t_path)
    data_name = 'download.tsv.{}.tar.bz2'.format(data)

    if(exists(s_path + 'download.tsv.{}.tar.bz2'.format(data))):
        return

    url = 'http://konect.cc/files/{}'.format(data_name)
    # 请求下载地址，以流式的。打开要下载的文件位置。
    with get(url, stream=True) as r, open(s_path + data_name, 'wb') as file:
        total_size = int(r.headers['content-length'])
        content_size = 0
        plan = 0
        start_time = time()
        temp_size = 0
        # 开始下载每次请求1024字节
        for content in r.iter_content(chunk_size=1024):
            file.write(content)
            # 统计已下载大小
            content_size += len(content)
            # 计算下载进度
            plan = '{:.4}'.format((content_size / total_size) * 100)
            # 每一秒统计一次下载量
            if time() - start_time > 1:
                start_time = time()
                speed = content_size - temp_size
                # KB级下载速度处理
                if 0 <= speed < (1024 ** 2):
                    print(plan, '%', speed / 1024, 'KB/s')
                # MB级下载速度处理
                elif (1024 ** 2) <= speed < (1024 ** 3):
                    print(plan, '%', speed / (1024 ** 2), 'MB/s')
                # GB级下载速度处理
                elif (1024 ** 3) <= speed < (1024 ** 4):
                    print(plan, '%', speed / (1024 ** 3), 'GB/s')
                # TB级下载速度处理
                else:
                    print(plan, '%', speed / (1024 ** 4), 'TB/s')


if __name__ == '__main__':
    print('test for getting detasets')
    data_list, data_len, useful_dataset_num = get_datasets()
    print(data_list[:3])
