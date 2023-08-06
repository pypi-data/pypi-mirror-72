# python3.7
# encoding: utf-8
"""
@author: Chenjin.Qian
@email:  chenjin.qian@xquant.com
@file:   get_data.py
@time:   2020-06-30 8:58
"""

import time


def format_date(x):
    day = str(int(x[0])) if int(x[0]) > 9 else f"0{str(x[0])}"
    month = str(int(x[1])) if int(x[1]) > 9 else f"0{str(x[1])}"
    date = f"{x[-1]}-{month}-{day}"
    return date


class GetHoliday(object):
    def __init__(self, year=None):
        self.cyear = time.strftime("%Y") if not year else year
        self.month = int(time.strftime("%m"))
        self.host = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?"
        self.params = [
            "resource_id=39043",
            "tn=wisetpl",
        ]
        self.df = self.get_year_source()

    def get_year_source(self, year=None):
        import requests
        year = year if year else self.cyear
        data = []
        for i in (2, 5, 8, 11):
            rdata = requests.get(f"{self.host}query={year}年{i}月&" + "&".join(self.params)).text
            datai = eval(rdata)["data"][0]["almanac"]
            data += datai
        import pandas as pd
        df = pd.DataFrame(data)
        df.drop(labels=["animal", "avoid", "gzDate", "gzMonth", "gzYear", "isBigMonth", "lunarDate",
                        "lunarMonth", "lunarYear", "oDate", "suit", "term", "type", "value"], axis=1, inplace=True)
        df["date"] = df[["day", "month", "year"]].apply(lambda x: format_date(x), axis=1)
        df["desc"].fillna("-", inplace=True)
        df["status"].fillna("-", inplace=True)
        df["status"] = df[["cnDay", "status"]].apply(
            lambda x: x[1] if x[1] != "-" else 3 if x[0] in ("六", "日") else 0, axis=1)
        df.drop_duplicates(inplace=True)
        return df

    def today_holiday(self):
        df = self.df
        status = df[df["date"] == time.strftime("%Y-%m-%d")]["status"]
        flag = int(status)
        return flag

    def anyday_holiday(self, date):
        df = self.df
        status = df[df["date"] == date]["status"]
        flag = int(status)
        return flag

    def get_holidays(self):
        df = self.df
        date_list = df[df["status"] == "1"]["date"].tolist()
        return date_list

    def get_workday(self):
        df = self.df
        oday = df[df["status"] != "1"]
        oday.reset_index(inplace=True)
        return oday
