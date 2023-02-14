import django
import os
import json
import praw
import datetime
import pytz


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toxit_main.settings')
    django.setup()
    #any code you want to run in the terminal goes here. This will not start a server like manage.py will

    from toxit.models import Inference_task

    inf = Inference_task.objects.get(id=22)

    mods, authors = inf.get_unique_edge_pairs()

    print(mods)
    print(authors)


if __name__ == '__main__':
    main()
