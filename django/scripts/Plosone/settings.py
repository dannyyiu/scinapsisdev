# -*- coding: utf-8 -*-

# Scrapy settings for Plosone project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

# Setting up django's project full path.
import sys
sys.path.insert(0, 'C:\\Python27\\scinapsis')

# Setting up django's settings module name.
# This module is located at C:\Python27\scinapsis\scinapsis\settings.
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'scinapsis.settings'

import django
django.setup()

BOT_NAME = 'Plosone' ###set to path name

SPIDER_MODULES = ['Plosone.spiders'] ###
NEWSPIDER_MODULE = 'Plosone.spiders' ###

