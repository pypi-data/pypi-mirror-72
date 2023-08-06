import tzlocal
import pytz
import elist.elist as elel
from pynoz.primitive import undefined,null,true,false
from pynoz.orb import Orb,set_via_pl_from_root
from datetime import datetime,timedelta,timezone

TO_AN_MD = {
    "+":'___',   
    "-":'__' 
}


FROM_AN_MD = {
    '___':'+',
    '__':'-'
}


def zone_to_an_map_func(zone):
    an = zone.replace('+','___')
    an = an.replace('-','__')
    return(an)

def an_to_zone_map_func(an):
    zone = an.replace('___','+')
    zone = zone.replace('__','-')
    return(zone)

def zone_to_an_arr_map_func(zone_arr):
    return(elel.mapv(zone_arr,zone_to_an_map_func))

def an_to_zone_arr_map_func(an_arr):
    return(elel.mapv(an_arr,an_to_zone_map_func))

    
def an_arr_to_leaf(an_arr):
    zone_arr = an_to_zone_arr_map_func(an_arr)
    s = elel.join(zone_arr,'/')
    s = an_to_zone_map_func(s)
    return(s)


def creat_timezones_prompt_orb():
    root = Orb()
    all_timezones = pytz.all_timezones
    arr = elel.mapv(all_timezones,lambda ele:ele.split('/'))
    arr = elel.mapv(arr,lambda ele:zone_to_an_arr_map_func(ele))
    arr.sort()
    for i in range(len(arr)):
        pl = arr[i]
        set_via_pl_from_root(root,pl,an_arr_to_leaf)
    return(root)

def zone2z(zone):
    tmzone = pytz.timezone(zone)
    utc_dt = datetime(1, 1, 1, 0, 0, 0, 000000, tzinfo=tmzone)
    z = datetime.strftime(utc_dt,"%z")
    return(z)

def creat_zmd():
    md = {}
    all_timezones = pytz.all_timezones
    for i in range(len(all_timezones)):
       zone = all_timezones[i] 
       z = zone2z(zone)
       md[zone] = z
       md[z] = zone
    return(md)


def creat_an_zmd():
    md = {}
    all_timezones = pytz.all_timezones
    for i in range(len(all_timezones)):
       zone = all_timezones[i]
       an = zone_to_an_map_func(zone) 
       z = zone2z(zone)
       md[an] = z
       md[z] = an
    return(md)


def creat_an_zone_md():
    md = {}
    all_timezones = pytz.all_timezones
    for i in range(len(all_timezones)):
       zone = all_timezones[i]
       an = zone_to_an_map_func(zone)
       md[zone] = an
       md[an] = zone
    return(md)



ZONES_PROMPT = creat_timezones_prompt_orb()
ZONES_Z_MD = creat_zmd()
AN_Z_MD = creat_an_zmd()
AN_ZONE_MD = creat_an_zone_md() 


def zone2dict(zone):
    tmzone = pytz.timezone(zone)
    utc_dt = datetime(1, 1, 1, 0, 0, 0, 000000, tzinfo=tmzone)
    z = datetime.strftime(utc_dt,"%z")
    tmdelta = utc_dt.utcoffset()
    tmzone = timezone(tmdelta,zone)
    utc_dt = utc_dt.replace(tzinfo=tmzone)
    soffset = tmdelta.total_seconds()
    tzname = utc_dt.tzname()
    d = {
        'z':z,
        'tzname':tzname,
        'zone':zone,
        'soffset':soffset,
        'msoffset':soffset * 1000,
    }
    return(d)


def utcoffset2tmzone(offset):
    delta = timedelta(0,offset) if(offset>=0) else timedelta(-1,86400+offset)
    tmzone = timezone(delta,'GMT')
    return(tmzone)


def z2offset(z):
    sign = z[0]
    h = int(z[1:3])
    min = int(z[3:5])
    offset = h*3600 + min * 60
    offset = offset if(sign=='+') else -offset
    return(offset)

def z2tmzone(z):
    offset = z2offset(z)
    tmzone = utcoffset2tmzone(offset)
    return(tmzone)

def zone2tmzone(zone):
    global AN_Z_MD
    global ZONES_Z_MD
    z = '+0000'
    if(zone in AN_Z_MD):
        z = AN_Z_MD[zone]
    elif(zone in ZONES_Z_MD):
        z = ZONES_Z_MD[zone]
    else:
        return(None)
    return(z2tmzone(z))


def dict2tmzone(d):
    return(utcoffset2tmzone(d['soffset']))



def get_soffset_from_tmzone(tmzone):
    dt = datetime(1, 1, 1, 0, 0, 0, 000000, tzinfo=tmzone)
    delta = dt.utcoffset()
    return(delta.total_seconds())
