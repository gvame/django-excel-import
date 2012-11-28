#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.urlresolvers import reverse
from guardian.admin import GuardedModelAdmin

from cityapp.apps.city_viewer.models import *
from cityapp.apps.city_viewer.utils import *

class AreaAdmin(GuardedModelAdmin):
   actions = ['export_db']
   def export_db(self, request, queryset):
       if len(queryset) > 1:
           self.message_user(request, "一次只能导出一个城市的数据")
       else:
           en_name = queryset[0].en_name
           export_city_sql(en_name)
           export_city_db(en_name)
           export_city_tips_html(en_name)
           self.message_user(request, "导出数据成功")

   export_db.short_description = '导出数据库'

class PlaceAdmin(GuardedModelAdmin):
    search_fields = ['zh_name','en_name']
    search_fields_verbose = ['中文名','英文名']

class TopicAdmin(GuardedModelAdmin):
    pass

class PictureAdmin(GuardedModelAdmin):
    search_fields = ['file_name']
    search_fields_verbose = ['文件名']

from tinymce.widgets import TinyMCE

class TripTipAdmin(GuardedModelAdmin):
    search_fields = ['title']
    search_fields_verbose = ['主题']
    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js',
              '/static/js/tiny_mce/tiny_mce.js',]

class OfflineMapAdmin(GuardedModelAdmin):
    pass

class APPInfoAdmin(GuardedModelAdmin):
    list_display = ('name', 'area', 'sell_date', 'liked_num', 'installed_num')

    def liked_num(self, obj):
        return APPLike.objects.liked_num(obj.area)
    liked_num.short_description = '喜欢数'

    def installed_num(self, obj):
        return APPInstall.objects.device_num(obj.area)
    installed_num.short_description = '安装数'

class APPReviewAdmin(GuardedModelAdmin):
    list_display = ('title', 'app', 'content', 'contact', 'ip_address', 'source', 'created_at')
    list_filter = (
        ('app'),
    )

class APPInstallAdmin(GuardedModelAdmin):
    list_display = ('device',)


admin.site.register(Area, AreaAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(TripTip, TripTipAdmin)
admin.site.register(OfflineMap, OfflineMapAdmin)
admin.site.register(APPInfo, APPInfoAdmin)
admin.site.register(APPReview, APPReviewAdmin)
admin.site.register(APPInstall, APPInstallAdmin)