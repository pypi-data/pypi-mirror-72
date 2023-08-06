import os
import json
with open("\\".join(os.path.abspath(__file__).split("\\")[:-1])+"\\"+"citys2.py","rb") as f:
    province_city_xian=json.loads(f.read())
def get_province_num(txt,province,pp_city=False,pp_xian=False):
    zong={}
    zong["xian_num"]={}
    zong["city_num"]={}
    zong["province_num"]={}

    h_province=province
    province_num=txt.count(h_province)*35

    citys_sort=[]
    for city in [pp_city] if pp_city else [citys for citys in province_city_xian[province] if citys!="self"]:
        if city[-1] in ["市","县","州","旗","镇","乡","岛"] and len(city)>2:
            h_city=city[:-1]
        else:
            h_city=city

        if pp_xian:
            if h_city[-2:] in ["街道","自治"] and len(h_city)>3:
                h_city=h_city[:-2]
        else:
            if h_city[-2:] in ["自治"] and len(h_city)>3:
                h_city=h_city[:-2]

        city_num=txt.count(h_city)*10

        if h_city!=h_province:
            province_num+=city_num
        else:
            city_num=city_num-1

        xians_sort=[]
        for xian in [xians for xians in province_city_xian[province][city] if xians!="self"]:
            if pp_xian and xian[-1] in ["区","市","县","州","旗","镇","乡","岛"] and len(xian)>2:
                h_xian=xian[:-1]
            elif xian[-1] in ["市","县","州","旗","镇","乡","岛"] and len(xian)>2:
                h_xian=xian[:-1]
            else:
                h_xian=xian

            if pp_xian:
                if h_xian[-2:] in ["街道","自治"] and len(h_xian)>3:
                    h_xian=h_xian[:-2]
            else:
                if h_xian[-2:] in ["自治"] and len(h_xian)>3:
                    h_xian=h_xian[:-2]

            xian_num=txt.count(h_xian)*5
            if h_xian!=h_province:
                province_num+=xian_num
            else:
                xian_num=xian_num-1

            if h_xian!=h_city:
                city_num+=xian_num
            else:
                xian_num=xian_num-1

            xians_sort.append({"xian":xian,"xian_num":xian_num})


        xian_sort=sorted(xians_sort,key=lambda ls:ls["xian_num"],reverse=True)[0] if xians_sort else {"xian":None,"xian_num":0}
        xian_sort["city"]=city
        xian_sort["city_num"]=city_num        
        citys_sort.append(xian_sort)

    city_sort=sorted(citys_sort,key=lambda ls:ls["city_num"]+ls["xian_num"],reverse=True)[0]
    city_sort["province"]=province
    city_sort["province_num"]=province_num
    return city_sort
def get_city(txt,h_zd=False):
    txt=txt.replace("北京时间","").replace(" ","").replace("\r","").replace("\t","").replace("\n","")
    h_zd=h_zd.replace("北京时间","").replace(" ","").replace("\r","").replace("\t","").replace("\n","") if h_zd else h_zd
    if h_zd:
        rs_lis=sorted([get_province_num(h_zd,province) for province in province_city_xian],key=lambda ls:ls["province_num"]+ls["city_num"]+ls["xian_num"],reverse=True)
        rs_li=rs_lis[0] if rs_lis[0]["province_num"] else sorted([get_province_num(h_zd,province,pp_xian=True) for province in province_city_xian],key=lambda ls:ls["province_num"]+ls["city_num"]+ls["xian_num"],reverse=True)[0]
        if rs_li["province_num"]:
            if rs_li["xian_num"]:
                return rs_li
            elif rs_li["city_num"]:
                jg=get_province_num(h_zd+txt,rs_li["province"],rs_li["city"])
                return jg if jg["xian_num"] else get_province_num(h_zd+txt,rs_li["province"],rs_li["city"],pp_xian=True)
            else:
                jg=get_province_num(h_zd+txt,rs_li["province"])
                return jg if jg["xian_num"] else get_province_num(h_zd+txt,rs_li["province"],pp_xian=True)
    rs_li=sorted([get_province_num(txt,province) for province in province_city_xian],key=lambda ls:ls["province_num"]+ls["city_num"]+ls["xian_num"],reverse=True)[0] 
    if rs_li["province_num"]:
        if rs_li["xian_num"]:
            return rs_li
        elif rs_li["city_num"]:
            return get_province_num(txt,rs_li["province"],rs_li["city"],pp_xian=True)
        else:
            return get_province_num(txt,rs_li["province"],pp_xian=True)
    else:
        rs_li=sorted([get_province_num(txt,province,pp_xian=True) for province in province_city_xian],key=lambda ls:ls["province_num"]+ls["city_num"]+ls["xian_num"],reverse=True)[0]
        return rs_li if rs_li["province_num"] else {}
