# -*- coding=utf-8 -*-
"""
  @author: laibo
  @time: 2019-02-22 21:25
"""
import time
from bs4 import BeautifulSoup
import urllib3

TYPE_MAP = {'点击量': 'www_www_all_suda_suda', '评论数': 'qbpdpl'}
BASIC_NEWS_URL = 'http://www.zaobao.com'

class RequestNews:

    @staticmethod
    def get_sina_news(top_type='day', top_show_num=10, top_order='DESC', top_cat='点击量', top_time=None):

        """
        获取新浪新闻
        :return:
        """
        data = {
            'top_type': top_type,
            'top_show_num': top_show_num,
            'top_order': top_order,
            'top_cat': TYPE_MAP[top_cat],
            'top_time': top_time if top_time else time.strftime("%Y%m%d", time.localtime())
        }
        response = urllib3.PoolManager().request(method='GET', url='http://top.news.sina.com.cn/ws/GetTopDataList.php',
                                                 fields=data)
        res_text = str(response.data).encode('utf-8').decode('unicode_escape')
        res_arr_str = res_text[res_text.index('['): res_text.rindex(']') + 1]
        res_arr = eval(res_arr_str)
        title_arr = ['%d.%s (%s【%s】);\n' % (
            i + 1, res_arr[i]['title'], res_arr[i]['media'], str(res_arr[i]['url']).replace('\\', '')) for i in
                     range(len(res_arr))]
        result = ['新浪新闻今日', top_cat, '排行：\n', "".join(title_arr)]
        return "".join(result)
        pass

    @staticmethod
    def get_zaobao_news():
        """
        获取联合早报新闻
        :return:
        """
        response = urllib3.PoolManager().request(method='GET', url='http://www.zaobao.com/news')
        soup = BeautifulSoup(response.data,features='html.parser')
        tab_pane = soup.find_all(id='Popular-daily')[0]
        result_arr = ["今日早报({0})：\n".format(time.strftime("%Y-%m-%d", time.localtime()))]
        index = 1
        for div in tab_pane.find_all(attrs={"typeof": "sioc:Item foaf:Document"}):
            result_arr.append(
                '%d.%s【%s】；\n' % (index, div.a.string, "".join([BASIC_NEWS_URL, str(div.a.attrs['href'])])))
            index += 1
        result_arr.append("-------------------------------------\n")
        result_arr.append("数据来源：联合早报网")
        return "".join(result_arr)


if __name__ == '__main__':
    print(RequestNews.get_zaobao_news())