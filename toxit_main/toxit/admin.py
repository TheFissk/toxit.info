from django.contrib import admin

from .models import Inference_task, Subreddit_mod, Subreddit_result, Comment_result, Subreddit


admin.site.register(Subreddit_result)
admin.site.register(Inference_task)
admin.site.register(Subreddit_mod)
admin.site.register(Comment_result)
admin.site.register(Subreddit)