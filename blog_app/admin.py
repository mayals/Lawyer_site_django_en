from django.contrib import admin
from.models import Category,Post,Comment





admin.site.site_header ='Catgory Admin Panel'
admin.site.site_title ='Category Admin Panel'



class InlinePost(admin.StackedInline):
    model = Post
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        InlinePost,
    ]


class PostAdmin(admin.ModelAdmin):        
    fields = ('post_title','post_author','cat_fk','post_views_counter','post_status')
    list_display = ('post_title','post_author','cat_fk','post_views_counter','post_status','combine_post_title_and_Category')
    list_display_links = ('cat_fk', 'post_author')
    list_editable = ('post_title',)
    list_filter = ('post_author','cat_fk')
    search_fields = ('post_title','post_author__username','cat_fk__cat_title',)
    def combine_post_title_and_Category(self,obj):
        return f'{obj.post_title}-{obj.cat_fk}'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

