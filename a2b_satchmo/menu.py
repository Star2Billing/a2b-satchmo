from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import * #Menu
from admin_tools.menu.models  import *
#from admin_tools.menu.items import *

# to activate your custom menu add the following to your settings.py:
#
# ADMIN_TOOLS_MENU = 'a2b_satchmo.menu.CustomMenu'

class CustomMenu(Menu):
    """
    Custom Menu for a2b_satchmo admin site.
    """
    def __init__(self, **kwargs):
        Menu.__init__(self, **kwargs)
        self.children.append(items.MenuItem(
            title=_('Dashboard'),
            url=reverse('admin:index')
        ))
        self.children.append(items.AppList(
            title=_('Applications'),
            models=('a2b_satchmo.customer.models.Card',
                    'a2b_satchmo.customer.models.Language',
                    'a2b_satchmo.customer.models.Call')
        ))
        """
        self.children.append(items.AppList(
            title=_('Administration'),
            models=('django.contrib',)
        ))
        """
    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


class MyMenu(Menu):
    class Media:
        css = ('css/a2b_menu.css',)
        js = ('js/a2b_menu.js',)
    def __init__(self, **kwargs):
        super(MyMenu, self).__init__(**kwargs)
        self.children.append(
            MenuItem(title='Home', url=reverse('admin:index'))
        )
        self.children.append(
            AppListMenuItem(title='Applications')
        )
        self.children.append(
            MenuItem(
                title='Multi level menu item',
                children=[
                     MenuItem(title='Child 1'),
                     MenuItem(title='Child 2'),
                ] 
            ),
        )

"""
class MyMenu(Menu):
    class Media:
        css = ('css/menu.css',)
        js = ('js/menu.js',)
    def __init__(self, **kwargs):
        super(MyMenu, self).__init__(**kwargs)
        self.children.append(
            MenuItem(title='Home', url=reverse('admin:index'))
        )
        self.children.append(
            AppListMenuItem(title='Applications')
        )

class MyMenu(Menu):
    def __init__(self, **kwargs):
        super(MyMenu, self).__init__(**kwargs)
        self.children.append(items.MenuItem(
            title=_('Home'),
            url=reverse('admin:index')
        ))
        self.children.append(AppListMenuItem(
            title='Applications',
            exclude_list=('django.contrib',)
            ))

"""
