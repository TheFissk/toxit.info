from django.contrib import admin

from .models import Inference_task, Subreddit_mod, Subreddit_result, Mod_edge, Author_edge, Comment_result, Subreddit


admin.site.register(Inference_task)
admin.site.register(Subreddit_result)
admin.site.register(Mod_edge)
admin.site.register(Author_edge)
admin.site.register(Subreddit_mod)
admin.site.register(Comment_result)
admin.site.register(Subreddit)