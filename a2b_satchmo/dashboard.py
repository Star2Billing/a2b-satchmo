from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard.dashboards import *
from admin_tools.dashboard.models import *
from admin_tools.dashboard.modules import *
from admin_tools.dashboard.views import *
# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'a2b_satchmo.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for a2b_satchmo.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            title=_('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                {
                    'title': _('Return to site'),
                    'url': '/',
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Log out'),
                    'url': reverse('admin:logout')
                },
            ]
        ))
        
        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            include_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,
            title=_('Recent Actions'),
            limit=5
        ))
        """
        # append a feed module
        self.children.append(modules.Feed(
            column=2,
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            column=2,
            title=_('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))
        """
    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'a2b_satchmo.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for a2b_satchmo.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            models=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass

class MyDashboard(Dashboard):
    
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)        
        
        self.children.append(modules.LinkList(
            title=_('Quick links'),
            layout='inline',
            css_classes=['collapse close'],
            column=2,
            children=[
                {
                    'title': _('View site'),
                    'url': '/',
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Log out'),
                    'url': reverse('admin:logout')
                },
            ]
        ))
        # will only list the django.contrib apps
        self.children.append(modules.AppList(
            title='Administration',
            include_list=('django.contrib',),
            column=1,
            css_classes=['collapse', 'open'],
        ))
        # append an app list module for "Applications"
        self.children.append(modules.ModelList(
            title=_('Models'),
            include_list=('a2b_satchmo.customer.models.Card',
                          'a2b_satchmo.customer.models.Language',
                          'a2b_satchmo.customer.models.Call'),
            column=1,
            css_classes=['collapse', 'open'],
        ))
        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,            
            title=_('Recent Actions'),
            limit=5,
            css_classes=['collapse', 'open'],
        ))
        
        self.children.append(modules.Feed(
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            column=2,
            limit=5
        ))
        self.children.append(modules.Group(
            title="Group",
            display="tabs",
            column=1,
            css_classes=['collapse','open'],
            children=[
                modules.AppList(
                    #title='Administration',
                    include_list=('django.contrib',),
                    css_classes=['collapse','open'],
                ),
                modules.ModelList(
                    title=_('Models'),
                    include_list=('a2b_satchmo.customer.models.Card',
                          'a2b_satchmo.customer.models.Language',
                          'a2b_satchmo.customer.models.Call'),
                    css_classes=['collapse','open'],
                ),
            ]
        ))
        

        

