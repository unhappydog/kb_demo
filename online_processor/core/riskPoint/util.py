from datetime import datetime


class util(object):
    # 时间差
    def time_difference(self, starttime, endtime):
        if starttime>endtime:
            return False
        if isinstance(endtime,str):
            if ':' in endtime:
                endtime = datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
            else:
                endtime = datetime.strptime(endtime, "%Y-%m-%d")
        if isinstance(starttime,str):
            if ':' in starttime:
                starttime = datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
            else:
                starttime = datetime.strptime(starttime, "%Y-%m-%d")
        diff = (endtime - starttime).days
        start = int("".join(datetime.strftime(starttime, '%Y')))
        end = int("".join(datetime.strftime(endtime, '%Y')))
        year = 0
        month = 0
        while start <= end:
            if self.is_leap(start):
                year = diff // 366
                month = diff % 366 // 30 + 2
                if month >= 12:
                    year = year + 1
                    month = month % 12
            else:
                year = diff // 365
                month = diff % 365 // 30 + 2
                if month >= 12:
                    year = year + 1
                    month = month % 12
            start += 1
        return year, month

    def is_leap(self, years):
        if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):  # 判断是否是闰年
            return True
        else:
            return False

    # 时间是否有交叉
    def overlapping(self, a_start, a_end, b_start, b_end):
        """
        :param a: worktime
        :param b:edutime
        """
        if max(a_start, b_start) < min(a_end, b_end):
            return True
        else:
            return False

    def gap(self, epchodata, updatetime, flag):
        endtime = ''
        starttime = ''
        if flag == 0:
            starttime = 'educationStartTime'
            endtime = 'educationEndTime'
        elif flag == 1:
            starttime = 'workStartTime'
            endtime = 'workEndTime'
        yearlist = []
        monthlist = []
        if len(epchodata) > 1:
            for edu in range(len(epchodata)-1, 0, -1):
                if epchodata[edu][endtime] != '':
                    gapend = epchodata[edu][endtime]
                else:
                    gapend = updatetime
                gapstart = epchodata[edu - 1][starttime]
                if not isinstance(self.time_difference(gapend,gapstart),bool):
                    year, month = self.time_difference(gapend, gapstart)
                    yearlist.append(year)
                    monthlist.append(month)
        return yearlist, monthlist


    def iszero(self,newput):
        count=0
        for i in newput:
            if i == 0:
                count += 1
            else:
                continue
        if count == len(newput):
            return True
        else:
            return False




if __name__ == '__main__':
    a_start = datetime(2017, 2, 1, 0, 0)
    b_start = datetime(2009, 6, 1, 0, 0)
    a_end = datetime(2019, 2, 1, 0, 0)
    b_end = datetime(2015, 6, 1, 0, 0)
    ss = util().overlapping(a_start, a_end, b_start, b_end)
    print(ss)
