# encoding=utf8

import csv
import os
import datetime
import matplotlib.pyplot as plt


def is_ok(now_av, pre_avs):
    res = False
    pos = 0.0
    neg = 0.0
    for i, av in enumerate(pre_avs[:-1]):
        if pre_avs[i + 1] > av:
            pos += 1
        else:
            neg += 1
    av_ratio = (now_av - min(pre_avs)) / min(pre_avs)
    pos_ratio = pos / (pos + neg)
    # print av_ratio, pos_ratio
    if av_ratio > 0.015 and pos_ratio > 0.8:
        res = True
    return res


def process(file):
    total_money = 0.0
    pre_money = 0.0
    first_begin = 0.0
    has = 0
    don_know = 0

    with open(file) as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)
        next(reader)
        x1, y1 = [i + 1 for i in range(240 * 4 + 60)], []
        x2, y2 = [i + 1 for i in range(240 * 4 + 60)], []
        sum_volume, sum_amount = 0.0, 0.0
        pre_day = datetime.datetime(1000, 1, 1)
        for i, line in enumerate(reader):
            # get raw data
            if len(line) < 8:
                continue
            day = datetime.datetime.strptime(line[0], '%Y/%m/%d')
            hour = datetime.datetime.strptime(line[1], '%H%M')
            # if day < datetime.datetime(2021, 1, 20):
            #     continue
            # if day > datetime.datetime(2021, 2, 10):
            #     continue
            begin = float(line[2])
            max_p = float(line[3])
            min_p = float(line[4])
            end = float(line[5])
            volume = float(line[6])
            amount = float(line[7])

            # calculate mean_av
            if day != pre_day:
                sum_volume, sum_amount = 0.0, 0.0
                pre_day = day
            sum_amount += amount
            sum_volume += volume
            mean_av = sum_amount / (sum_volume + 1)

            y1.append(begin)
            y2.append(mean_av)

            # judge mean_av
            if hour == datetime.datetime(1900, 1, 1, 10, 30):
                # draw)

                if len(y1) == 240 * 4 + 60:
                    if first_begin == 0:
                        first_begin = begin
                    plt.plot(x1, y1)
                    plt.plot(x2, y2)
                    for axv in range(1, 5):
                        plt.axvline(x=240 * axv)
                    plt.show()
                    if has == 1:
                        print '您赚%f，购入第一股后一直持有赚%f，日期%s' % (
                        (total_money + begin) / first_begin, (-first_begin + begin) / first_begin, day)
                    else:
                        print '您赚%f，购入第一股后一直持有赚%f，日期%s' % (
                        (total_money) / first_begin, (-first_begin + begin) / first_begin, day)
                    if has == 0:
                        print '持有？',
                        buy = int(input())
                        if buy == 1:
                            has += 1
                            total_money -= begin
                            pre_money = begin
                    elif has == 1:
                        put_value = (begin - pre_money) * 100
                        if put_value > 0:
                            print '本次购买已赚了%f钱，继续持有？' % put_value,
                        else:
                            print '本次购买亏了%f钱，还继续持有吗？' % put_value,
                        buy = int(input())
                        if buy == 0:
                            has -= 1
                            total_money += begin
                    y1 = y1[240:]
                    y2 = y2[240:]


if __name__ == '__main__':
    process('./data/SZ#002739.txt')
