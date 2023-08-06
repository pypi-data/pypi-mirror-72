#y            year                  年
#m            month                 月
#d            day                   日
#h            hour                  小时
#min          minute                分
#s            second                秒
#ms           microsecond           毫秒

#ts           timestamp             整数到秒
#mts          timestamp             整数到毫秒
#tz           timezone              时区名字
#soffset       timezone-seconds-offset       时区偏移    utc + offset = local
#msoffset       timezone-microseconds-offset       时区偏移    utc + offset = local


#yq           quarter-of-year        每年第几季
#yw           week-of-year           每年第几周
#yd           day-of-year            每年第几天


#qm           month-of-quarter        每季第几月
#qw           week-of-quarter         每季第几周
#qd           day-of-quarter          每季第几天

#mt           ten-of-month            每月第几旬
#mw           week-of-month           每月第几周


#wd           isoweekday                 星期几  星期日是7


#dt           daytime


import time
from datetime import datetime,timedelta,timezone
import pytz
import calendar
from pynoz.tz import zone2dict,ZONES_Z_MD,utcoffset2tmzone,get_soffset_from_tmzone 
from pynoz.tz import z2offset,z2tmzone,zone2tmzone
from pynoz.tz import dict2tmzone as tzdict2tmzone
from datetime import date as datetme_date
import efuntool.efuntool as eftl



DICT_KL = ['y', 'm', 'd', 'h', 'min', 's', 'ms', 'ts', 'mts', 'tzname', 'soffset', 'msoffset', 'yq', 'yw', 'yd', 'qm', 'qw', 'qd', 'mt', 'mw', 'td', 'wd']


DATE_FMT_MD = { 
    '%a, %d %b %Y %H:%M:%S GMT':'rfc1123',
    '%d %b %Y %H:%M:%S GMT':'rfc1123_nowkday',
    '%a, %d %b %Y %H:%M:%S':'rfc1123_notz',
    '%a, %d %b %Y %H:%M:%S %z':'rfc1123_tzoffset',
    '%a, %d-%b-%Y %H:%M:%S GMT':'rfc1123_hypen',
    '%A, %d-%b-%y %H:%M:%S GMT':'rfc850',
    '%d-%b-%y %H:%M:%S GMT':'rfc850_nowkday',
    '%a, %d-%b-%y %H:%M:%S GMT':'rfc850_a',
    '%A, %d-%b-%Y %H:%M:%S GMT':'rfc850_broken',
    '%d-%b-%Y %H:%M:%S GMT':'rfc850_broken_nowkday',
    '%a, %b %d %H:%M:%S %Y':'asctime',
    '%Y-%m-%d %H:%M:%S %z':'iso8601',
    "%a %b %d %Y %H:%M:%S %Z%z":'abdYHMSZz',
    "%a %b %d %Y %H:%M:%S":'abdYHMS',
    "%Y-%m-%dT%H:%M:%S.%fZ":'nodejs',
    "%Y-%m-%d %H:%M:%S.%f":'YmdHMSf',
    "%Y-%m-%d %H:%M:%S.%f %Z%z":'YmdHMSfZz',
    '%Y-%m-%d %H:%M:%S %Z %z':'YmdHMSZz',
    'rfc1123': '%a, %d %b %Y %H:%M:%S GMT',
    'rfc1123_nowkday': '%d %b %Y %H:%M:%S GMT',
    'rfc1123_notz': '%a, %d %b %Y %H:%M:%S',
    'rfc1123_tzoffset': '%a, %d %b %Y %H:%M:%S %z',
    'rfc1123_hypen': '%a, %d-%b-%Y %H:%M:%S GMT',
    'rfc850': '%A, %d-%b-%y %H:%M:%S GMT',
    'rfc850_nowkday': '%d-%b-%y %H:%M:%S GMT',
    'rfc850_a': '%a, %d-%b-%y %H:%M:%S GMT',
    'rfc850_broken': '%A, %d-%b-%Y %H:%M:%S GMT',
    'rfc850_broken_nowkday': '%d-%b-%Y %H:%M:%S GMT',
    'asctime': '%a, %b %d %H:%M:%S %Y',
    'iso8601': '%Y-%m-%d %H:%M:%S %z',
    'abdYHMSZz': '%a %b %d %Y %H:%M:%S %Z %z',
    'abdYHMS': '%a %b %d %Y %H:%M:%S',
    'nodejs': '%Y-%m-%dT%H:%M:%S.%fZ',
    'YmdHMSf': '%Y-%m-%d %H:%M:%S.%f',
    'YmdHMSfZz': '%Y-%m-%d %H:%M:%S.%f %Z %z',
    'YmdHMSZz': '%Y-%m-%d %H:%M:%S %Z %z',
}

NAME_TO_FMT_DICT = {
    'rfc1123': '%a, %d %b %Y %H:%M:%S GMT',
    'rfc1123_nowkday': '%d %b %Y %H:%M:%S GMT',
    'rfc1123_notz': '%a, %d %b %Y %H:%M:%S',
    'rfc1123_tzoffset': '%a, %d %b %Y %H:%M:%S %z',
    'rfc1123_hypen': '%a, %d-%b-%Y %H:%M:%S GMT',
    'rfc850': '%A, %d-%b-%y %H:%M:%S GMT',
    'rfc850_nowkday': '%d-%b-%y %H:%M:%S GMT',
    'rfc850_a': '%a, %d-%b-%y %H:%M:%S GMT',
    'rfc850_broken': '%A, %d-%b-%Y %H:%M:%S GMT',
    'rfc850_broken_nowkday': '%d-%b-%Y %H:%M:%S GMT',
    'asctime': '%a, %b %d %H:%M:%S %Y',
    'iso8601': '%Y-%m-%d %H:%M:%S %z',
    'abdYHMSZz': '%a %b %d %Y %H:%M:%S %Z %z',
    'abdYHMS': '%a %b %d %Y %H:%M:%S',
    'nodejs': '%Y-%m-%dT%H:%M:%S.%fZ',
    'YmdHMSf': '%Y-%m-%d %H:%M:%S.%f',
    'YmdHMSfZz': '%Y-%m-%d %H:%M:%S.%f %Z %z',
    'YmdHMSZz':'%Y-%m-%d %H:%M:%S %Z %z'
}

FMT_TO_NAME_DICT = {
    '%a, %d %b %Y %H:%M:%S GMT':'rfc1123',
    '%d %b %Y %H:%M:%S GMT':'rfc1123_nowkday',
    '%a, %d %b %Y %H:%M:%S':'rfc1123_notz',
    '%a, %d %b %Y %H:%M:%S %z':'rfc1123_tzoffset',
    '%a, %d-%b-%Y %H:%M:%S GMT':'rfc1123_hypen',
    '%A, %d-%b-%y %H:%M:%S GMT':'rfc850',
    '%d-%b-%y %H:%M:%S GMT':'rfc850_nowkday',
    '%a, %d-%b-%y %H:%M:%S GMT':'rfc850_a',
    '%A, %d-%b-%Y %H:%M:%S GMT':'rfc850_broken',
    '%d-%b-%Y %H:%M:%S GMT':'rfc850_broken_nowkday',
    '%a, %b %d %H:%M:%S %Y':'asctime',
    '%Y-%m-%d %H:%M:%S %z':'iso8601',
    "%a %b %d %Y %H:%M:%S %Z%z":'abdYHMSZz',
    "%a %b %d %Y %H:%M:%S":'abdYHMS',
    "%Y-%m-%dT%H:%M:%S.%fZ":'nodejs',
    "%Y-%m-%d %H:%M:%S.%f":'YmdHMSf',
    "%Y-%m-%d %H:%M:%S.%f %Z%z":'YmdHMSfZz',
    '%Y-%m-%d %H:%M:%S %Z %z':'YmdHMSZz'
}



def get_yq_via_m(m):
    m = m -1
    return((m - m % 3)//3+1)

def get_days_num_of_year(y):
    cond = calendar.isleap(y)
    return(366 if(cond) else 365)

def get_yw(y,m,d):
    date = datetme_date(y,m,d)
    t = date.isocalendar()
    return(t[1])


def get_days_num_of_month(y,m):
    t = calendar.monthrange(y,m)
    return(t[1])

def get_yd(y,m,d):
    '''
        from 1 to 365/266
    '''
    yd = 0 
    for i in range(1,m):
        yd = yd + get_days_num_of_month(y,i)
    yd = yd + d
    return(yd)

def get_qm(m):
    return(m%3 if(m%3) else 3)

def get_fst_date_of_q(y,q):
    if(q==1):
        return(datetme_date(y,1,1))
    elif(q==2):
        return(datetme_date(y,4,1))
    elif(q==3):
        return(datetme_date(y,7,1))
    else:
        return(datetme_date(y,10,1))


def get_qw(y,q,m,d):
    fst_date = get_fst_date_of_q(y,q)
    fst_yw = fst_date.isocalendar()[1]
    yw = get_yw(y,m,d)
    qw = 1 + (yw - fst_yw)
    return(qw)


def get_qd(y,q,m,d):
    fst_date = get_fst_date_of_q(y,q)
    fst_yd = get_yd(fst_date.year,fst_date.month,fst_date.day)
    yd = get_yd(y,m,d)
    qd = 1 + (yd - fst_yd)
    return(qd)


def get_mt(m,d):
    if(d>=1 and d<=10):
        return(1)
    elif(d>=10 and d<=20):
        return(2)
    else:
        return(3)


def get_fst_date_of_m(y,m):
    return(datetme_date(y,m,1))


def get_mw(y,m,d):
    fst_date = get_fst_date_of_m(y,m)
    fst_yw = fst_date.isocalendar()[1]
    yw = get_yw(y,m,d)
    mw = 1 + (yw - fst_yw)
    return(mw)


def get_td(y,m,d):
    t = get_mt(m,d)
    if(t == 1):
        return(d)
    elif(t ==2):
        return(d-10)
    else:
        return(d-20)



def dt2dict(dt):
    global DICT_KL
    y = dt.year
    m = dt.month 
    d = dt.day 
    h = dt.hour
    min = dt.minute
    s = dt.second
    ms = dt.microsecond * 1000
    ts = dt.timestamp()
    mts = ts * 1000
    tzname = dt.tzname()
    tzname = 'GMT' if(tzname == None) else tzname
    z = dt.strftime('%z')
    z = '+0000' if(z == '') else z
    zone = ZONES_Z_MD[z] if(z!='+0000') else 'GMT'
    delta = dt.utcoffset()
    delta = timedelta(0) if(delta == None) else delta
    soffset = delta.total_seconds()
    msoffset =  soffset * 1000
    yq = get_yq_via_m(m)
    date = dt.date()
    yw = date.isocalendar()[1]
    yd = get_yd(y,m,d)
    qm = get_qm(m)
    qw = get_qw(y,yq,m,d)
    qd = get_qd(y,yq,m,d)
    mt = get_mt(m,d)
    mw = get_mw(y,m,d)
    td = get_td(y,m,d)
    wd = dt.isoweekday()
    d = {
        "y":y,
        "m":m, 
        "d":d,
        "h":h,
        "min":min,
        "s":s,
        "ms":ms,
        "ts":ts,
        "mts":mts,
        "z":z,
        "zone":zone,
        "tzname":tzname,
        "soffset":soffset,
        "msoffset":msoffset,
        "yq":yq,
        "yw":yw,
        "yd":yd,
        "qm":qm,
        "qw":qw,
        "qd":qd,
        "mt":mt,
        "mw":mw,
        "td":td,
        "wd":wd,
    }
    return(d)

def dt2ts(dt):
    return(dt.timestamp())

def detect_fmt(s):
    global NAME_TO_FMT_DICT
    for name in NAME_TO_FMT_DICT:
        fmt = NAME_TO_FMT_DICT[name]
        try:
            datetime.strptime(s,fmt)
        except:
            pass
        else:
            return(fmt)
    return(None)

def dt2str(dt,fmt_or_name='YmdHMSZz'):
    global FMT_TO_NAME_DICT
    global NAME_TO_FMT_DICT
    #if its a valid fmt_name
    try:
        fmt = NAME_TO_FMT_DICT[fmt_or_name]
    except:
        pass
    else:
        return(dt.strftime(fmt))
    #if its a valid fmt
    try:
        s = dt.strftime(fmt_or_name)
    except:
        pass
    else:
        return(s)
    return(None)


def str2dt(s,fmt_or_name=None):
    global FMT_TO_NAME_DICT
    global NAME_TO_FMT_DICT
    if(fmt_or_name==None):
        try:
            fmt = detect_fmt(s)
        except:
            pass
        else:
            return(datetime.strptime(s,fmt))
    else:
        #if its a valid fmt_name
        try:
            fmt = NAME_TO_FMT_DICT[fmt_or_name]
        except:
            pass
        else:
            return(datetime.strptime(s,fmt))
        #if its a valid fmt
        try:
            fmt = fmt_or_name
        except:
            pass
        else:
            return(datetime.strptime(s,fmt))
        #
        return(None)


def str2dict(s,fmt_or_name=None):
    dt = str2dt(s,fmt_or_name)
    return(dt2dict(dt))

def str2ts(s,fmt_or_name=None):
    d = str2dict(s,fmt_or_name)
    return(d['ts'])


def zzo2tmzone(zzo):
    tmzone = None
    try:
        tmzone = utcoffset2tmzone(zzo)
    except:
        try:
            tmzone = zone2tmzone(zzo)
        except:
            try:
                tmzone = z2tmzone(zzo)
            except:
                pass
            else:
                pass
        else:
            pass
    else:
        pass
    return(tmzone)

def ts2dt(ts,zzo='GMT+0'):
    tmzone = zzo2tmzone(zzo)
    soffset = get_soffset_from_tmzone(tmzone)
    ts = ts - soffset
    utc_dt = datetime.fromtimestamp(ts)
    dt = utc_dt.replace(tzinfo=tmzone)
    return(dt)


def ts2dict(ts,zzo='GMT+0'):
    dt = ts2dt(ts,zzo)
    return(dt2dict(dt))


def ts2str(ts,**kwargs):
    zzo = eftl.dflt_kwargs('tz','GMT+0',**kwargs)
    fmt_or_name = eftl.dflt_kwargs('fmt','YmdHMSZz',**kwargs)
    dt = ts2dt(ts,zzo)
    s = dt2str(dt,fmt_or_name)
    return(s)

def dict2ts(d):
    return(d['ts'])

def dict2dt(d):
    ts = d['ts']
    zzo = d['z']
    dt = ts2dt(ts,zzo)
    return(dt)

def dict2str(d,fmt_or_name='YmdHMSfZz'):
    dt = dict2dt(d) 
    s = dt2str(dt,fmt_or_name)
    return(s)


