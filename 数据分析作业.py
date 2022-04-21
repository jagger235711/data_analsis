"""
 -*- coding: utf-8 -*-

 @Time : 2022/3/31 19:39

 @Author : jagger

 @File : 数据分析作业.py

 @Software: PyCharm 

 @contact: 252587809@qq.com


根据上课讲的吴迪老师的微信好友数据分析，请选择你的微信好友数据，或者你的qq好友数据，或者你的班级同学数据，或者其他你能获取的其他人物数据作为分析对象。然后利用上课讲的技术，但不限于，对其进行数据分析。比如分析微信好友数据，可以可视化好友男女比例分布，可视化省份来源，可视化签名的情感强度值等等。

要求：1分析数据用xls或者csv格式存储。

2.代码用py文件附件形式上传，方便我的下载。

3.在作业里可以介绍你的主要功能和可视化截图。

4.根据功能完整性和结果的酷给分。

 -*- 功能说明 -*-

"""
import csv

from pyecharts.charts import Scatter
from pyecharts.charts import Bar
from pyecharts.charts import Map
# 用于设值全局配置和系列配置
from pyecharts import options as opts
import xlrd
from collections import Counter

from pyecharts.commons.utils import JsCode
from snownlp import SnowNLP


def getcvsData(filenamelst, index):
    '''
    读取csv文件,把信息读取出来
    Parameters
    ----------
    filename : 文件名
    index : 列下标

    Returns
    -------

    '''
    lstdata = []
    for filename in filenamelst:
        data = []
        with open(filename, 'r') as fr:
            reader = csv.reader(fr)
            for i in reader:
                if i[0] == '':
                    continue
                elif i[index] == '延边':
                    res = '延吉'
                elif i[index] == '路环岛' or i[index] == '花地玛堂区':
                    res = '澳门'
                else:
                    res = i[index]
                data.append(res)
        lstdata.append(lstdata)

    return lstdata


def getxlsData(filenamelst, index):
    '''
    读取xls文件,把信息读取出来
    Parameters
    ----------
    filename :
    index :

    Returns
    -------

    '''
    lstdata = []
    for filename in filenamelst:
        data = []

        xls = xlrd.open_workbook_xls(filename)
        for table in xls.sheets():
            for i in table:
                if i[1].value != '序号' and not isinstance(i[index], str):
                    string = str(i[index].value).strip()
                    if string == '内蒙古自治区':
                        string = '内蒙古'
                    elif string == '广西壮族自治区':
                        string = '广西'
                    elif len(string) > 1 and (string[-1] == '省' or string[-1] == '市'):
                        string = string[:len(string) - 1]
                    data.append(string)
        lstdata.append(data)
    # lstdata.append(i[index].value)
    # print(lstdata)
    # print(len(lstdata[2]))
    return lstdata


def VisualPropyecharts(lstprovincelst):
    '''
    省份可视化
    Parameters
    ----------
    lstprovincelst : 数据列表

    Returns
    -------

    '''
    M = (
        Map(init_opts=opts.InitOpts(width='full'))
            .add("17级的学生数据", Counter(lstprovincelst[0]).most_common(), 'china')
            .add("18级的学生数据", Counter(lstprovincelst[1]).most_common(), 'china')
            .add("19级的学生数据", Counter(lstprovincelst[2]).most_common(), 'china')
            .set_global_opts(
            title_opts=opts.TitleOpts(title="省份数据"),
            visualmap_opts=opts.VisualMapOpts(max_=15, is_piecewise=True, border_width=1)
        )

    ).render("map-学生省份.html")


def VisualSexpyechart(lstsexlst):
    '''
    性别可视化
    Parameters
    ----------
    lstsex :

    Returns
    -------

    '''
    sex = []
    for lstsex in lstsexlst:
        sex.append(Counter(lstsex))
    print(sex)
    bar = (
        Bar()
            .add_xaxis(
            [
                "17级学生数据",
                "18级学生数据",
                "19级学生数据",
            ]
        )
            .add_yaxis('男生', [sex[0].get('男'), sex[1].get('男'), sex[2].get('男')])
            .add_yaxis('女生', [sex[0].get('女'), sex[1].get('女'), sex[2].get('女')])
            .set_global_opts(
            title_opts=opts.TitleOpts(title='学生性别分析'),
            yaxis_opts=opts.AxisOpts(name="人数"),
            # xaxis_opts=opts.AxisOpts(name="性别")
        )

    ).render('学生性别分析.html')


def mood():
    xlslst = ['软件17学生详细名单.xls']
    lstnamelst = getxlsData(xlslst, 3)
    lstmottolst = getxlsData(xlslst, 10)
    mottoDic = {}
    for namelst, mottolst in zip(lstnamelst, lstmottolst):
        for name, motto in zip(namelst, mottolst):
            name = str(name).strip()
            motto = str(motto).strip()
            mottoDic[name] = SnowNLP(motto).sentiments
    # print(mottoDic)

    mottoKey = []
    mottoValue = []
    for i, j in mottoDic.items():
        mottoKey.append(i)
        mottoValue.append(j)

    # print()
    c = (
        Scatter(init_opts=opts.InitOpts(width='full'))
            .add_xaxis(mottoKey)
            # .add_yaxis("商家A", Faker.values())
            # .add_yaxis("商家B", Faker.values())
            # .add_yaxis('17')
            .add_yaxis('17级学生', mottoValue, label_opts=opts.LabelOpts(
            formatter=JsCode(
                # "function(params){return params.value[0] +' : '+ params.value[1];}"
                "function(params){return params.value[0];}"
            )
        ), )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="个性签名情感分析"),
            # visualmap_opts=opts.VisualMapOpts(type_="size", max_=1, min_=0),
            # tooltip_opts=opts.TooltipOpts(
            #     formatter=JsCode(
            #         "function (params) {return params.name + ' : ' + params.value[1];}"
            #     )
            # ),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True, ), name='情感值'),
            # legend_opts=opts.LegendOpts(type_='scroll', pos_left='left', orient='vertical')
        )
            .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_='average', name='数据平均值'),
                    opts.MarkLineItem(y=0.5, name='中值'),
                ]
            )
        )
    ).render("个性签名情感分析.html")


if __name__ == "__main__":
    xlslst = ['软件17学生详细名单.xls', '软件18学生详细名单.xls', '软件19学生详细名单.xls']
    VisualPropyecharts(getxlsData(xlslst, 6))  # 省份Map可视化
    # VisualSexpyechart(getxlsData(xlslst, 5))  # 性别Bar可视化
    # mood()
