# encoding=utf-8

def valid_express(express):
    valid = ['EMS', '顺丰']
    if express not in valid:
        express = 'others'
    return express

def valid_app(app):
    valid = ['1P_ThemeWallpapers', \
             '9P_RetinaWallpapers', \
             '9P_iOS7Wallpapershd', \
             '9P_iPhone5Wallpapers', \
             'AR_XianYouAnswer']
    if app not in valid:
        app = 'others'
    return app

def valid_model(model):
    valid = ['iPhone 4/4s 3D_磨砂', \
             'iPhone 4/4s 彩印', \
             'iPhone 4/4s 彩绘', \
             'iPhone 4/4s 浮雕', \
             'iPhone 4/4s 磨砂', \
             'iPhone 5/5s 3D_磨砂', \
             'iPhone 5/5s 彩印', \
             'iPhone 5/5s 彩绘', \
             'iPhone 5/5s 浮雕', \
             'iPhone 5/5s 磨砂', \
             'iPhone 5c 3D_磨砂', \
             'iPhone 5c 彩印', \
             'iPhone 5c 彩绘', \
             'iPhone 5c 浮雕']
    if model not in valid:
        model = 'others'
    return model

def valid_province(province):
    valid = ['北京', \
             '天津', \
             '河北', \
             '山西', \
             '内蒙古', \
             '辽宁', \
             '吉林', \
             '黑龙江', \
             '上海', \
             '江苏', \
             '浙江', \
             '安徽', \
             '福建', \
             '江西', \
             '山东', \
             '河南', \
             '湖北', \
             '湖南', \
             '广东', \
             '广西', \
             '海南', \
             '重庆', \
             '四川', \
             '贵州', \
             '云南', \
             '西藏', \
             '陕西', \
             '甘肃', \
             '青海', \
             '宁夏', \
             '新疆']
    for i in range(len(valid)):
        if valid[i] in province:
            province = valid[i]
            break
    if province not in valid:
        province = 'others'
    return province

def which_model(model):
    if '4/4' in model:
        if '磨砂' in model:
            model = 'iPhone4/4s 磨砂'
        elif '彩绘' in model:
            model = 'iPhone4/4s 彩绘'
        elif '彩印' in model:
            model = 'iPhone4/4s 彩印'
        elif '浮雕' in model:
            model = 'iPhone4/4s 浮雕'
    elif '5/5' in model:
        if '磨砂' in model:
            model = 'iPhone5/5s 磨砂'
        elif '彩绘' in model:
            model = 'iPhone5/5s 彩绘'
        elif '彩印' in model:
            model = 'iPhone5/5s 彩印'
        elif '浮雕' in model:
            model = 'iPhone5/5s 浮雕'
    elif '5c' in model or '5C' in model:
        if '磨砂' in model:
            model = 'iPhone5c 磨砂'
        elif '彩绘' in model:
            model = 'iPhone5c 彩绘'
        elif '彩印' in model:
            model = 'iPhone5c 彩印'
        elif '浮雕' in model:
            model = 'iPhone5c 浮雕'
    else:
        model = 'others'
    return model
    