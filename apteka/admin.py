from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from .models import *


admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(
    Catalog,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(
    Popular_brand,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)




admin.site.register(Personal_account)
admin.site.register(Product)
admin.site.register(MonthlyPromotion)
admin.site.register(Order)
admin.site.register(Health_blog)
