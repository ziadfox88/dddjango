from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','auther','publish','status'] #title head 
    list_filter = ['status', 'created', 'publish','auther']
    search_fields = ['title','body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ['auther']
    date_hierarchy = 'publish'
    ordering = ['status','publish']