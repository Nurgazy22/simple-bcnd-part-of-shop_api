from django.contrib import admin
from .models import Product, Category
from review.models import Comment



admin.site.register(Category)

class CommentInline(admin.TabularInline):
    model = Comment



class PoductAdmin(admin.ModelAdmin):
    list_filter = ['title', 'price']
    list_display = ['title', 'slug']
    search_fields = ['title', 'description']
    inlines = [CommentInline]


admin.site.register(Product, PoductAdmin)



