djangoTimepicker
=========================

**djangoTimepicker：** django 时间戳时间控件，可以在整数字段中使用该控件

功能
=========

- 支持整数格式添加时间控件
- 支持自定制时间格式以及时间控件语言显示类型

安装
=============

* Install
    > $ pip install djangoTimepicker

* add `djangoTimepicker` to your `INSTALLED_APPS` setting

使用
======

`app` `forms.py` 中导入 `DjangoTimePickerInput`，在 `ModelForm` 中需要添加时间控件的字段中使用该组件

    # models.py
    from django.db import models


    class Person(models.Model):
        name = models.CharField(max_length=32, blank=False)
        createdAt = models.BigIntegerField(verbose_name='创建时间', blank=True)

    # forms.py
    from django import forms

    from . models import Person

    from djangoTimepicker import DjangoTimePickerInput

    class PersonForm(forms.ModelForm):
        class Meta:
            model = Person

            fields = ('__all__')

            widgets = {
            'createdAt': DjangoTimePickerInput(timeFormat='YmdHis', language='zh')
            }

`app` `xadmin.py` 中导入 `PersonForm`

    import xadmin

    import .forms import PersonForm

    @xadmin.sites.register(User)

    class PersonModelAdmin(object):
    
        form = PersonForm

支持的时间格式(timeFormat)：
    
    Y:年 m:月 d:日  H:时 i:分 s:秒

支持的语言(language)：

    ar - Arabic

    az - Azerbaijanian (Azeri)

    bg - Bulgarian

    bs - Bosanski

    ca - Català

    ch - Simplified Chinese

    cs - Čeština

    da - Dansk

    de - German

    el - Ελληνικά

    en - English

    en-GB - English (British)

    es - Spanish

    et - "Eesti"

    eu - Euskara

    fa - Persian

    fi - Finnish (Suomi)

    fr - French

    gl - Galego

    he - Hebrew (עברית)

    hr - Hrvatski

    hu - Hungarian

    id - Indonesian

    it - Italian

    ja - Japanese

    ko - Korean (한국어)

    kr - Korean

    lt - Lithuanian (lietuvių)

    lv - Latvian (Latviešu)

    mk - Macedonian (Македонски)

    mn - Mongolian (Монгол)

    nl - Dutch

    no - Norwegian

    pl - Polish

    pt - Portuguese

    pt-BR - Português(Brasil)

    ro - Romanian
    
    ru - Russian

    se - Swedish

    sk - Slovenčina

    sl - Slovenščina

    sq - Albanian (Shqip)

    sr - Serbian Cyrillic (Српски)

    sr-YU - Serbian (Srpski)

    sv - Svenska

    th - Thai

    tr - Turkish

    uk - Ukrainian

    vi - Vietnamese

    zh - Simplified Chinese (简体中文)

    zh-TW - Traditional Chinese (繁體中文)

- Tips: 该项目引用 [datatimepicker](https://github.com/xdan/datetimepicker), [点击查看更多配置](https://xdsoft.net/jqplugins/datetimepicker/)

**实例展示**
- 时间格式：'YmdHis': 年月日时分秒

![image](https://github.com/DanielZhui/django-time-picker/blob/master/display/created.jpg)

- 时间格式：'Y-m-d H-i-s': 年-月-日 时-分-秒

![image](https://github.com/DanielZhui/django-time-picker/blob/master/display/createds.jpg)