import os
from jinja2 import FileSystemLoader, Environment

SITE_DIR = 'site'
PAGES_DIR = 'pages'
STATIC_DIR = 'static'
TEMPLATES_DIR = 'templates'
POSTS_DIR = 'posts'
common_template_variables = {
    # This can be commented out if you
    # don't want to have them show in your journal
    "your_name": "Y/N",
    "site_title": "Your site's title",
    "email_url": "your@email.com",
    "email_text": "your (at) email (dot) com",
    "twitter_url": "https://twitter.com/<username>",
    "github_url": "https://github.com/<username>",
    "gitlab_url": "https://gitlab.com/<username>",

}

templateLoader = FileSystemLoader(searchpath=TEMPLATES_DIR)
templateEnv = Environment(loader=templateLoader)

