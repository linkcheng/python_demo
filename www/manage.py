#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'www.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


"""
# 生成项目
django-admin.py startproject www
cd www
# 生成应用
django-admin.py startapp server
# 迁移数据库
python manage.py migrate
# 创建管理员
python manage.py createsuperuser --email admin@example.com --username admin
"""

if __name__ == '__main__':
    main()
