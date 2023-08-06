import logging

from django.contrib.postgres.fields import JSONField

from isc_common import getAttr
from isc_common.auth.models.user import User
from isc_common.auth.models.user_permission import User_permission
from isc_common.auth.models.usergroup import UserGroup
from isc_common.auth.models.usergroup_permission import Usergroup_permission
from isc_common.fields.code_field import CodeField
from isc_common.fields.description_field import DescriptionField
from isc_common.fields.name_field import NameField
from isc_common.http.DSRequest import DSRequest
from isc_common.managers.common_manager import CommonManager
from isc_common.models.audit import AuditModel

logger = logging.getLogger(__name__)


class Widgets_treesManager(CommonManager):
    def createFromRequest(self, request, printRequest=False):
        request = DSRequest(request=request)
        id = getAttr(request.json, 'id')
        table_name = getAttr(request.json, 'table_name')

        data = request.get_data()
        if getAttr(data, 'id_widget') == '/':
            data = getAttr(data, 'children')[0]

        id_widget = data.get('id_widget', None)

        if table_name == 'widgets_trees':
            name = data.get('name', None)
            class_name = data.get('class_name', None)
            description = data.get('description', None)
            res = super().update_or_create(
                id_widget=id_widget,
                defaults=dict(
                    id_widget=id_widget,
                    name=name,
                    class_name=class_name,
                    description=description,
                    structure=data
                )
            )
            return res[0]

        if table_name == 'user':
            user = User.objects.get(id=id)
            widget = Widgets_trees.objects.get(id_widget=id_widget)
            User_permission.objects.update_or_create(
                user=user,
                widget=widget,
                defaults=dict(
                    permission=data
                ))
            return dict()

        if table_name == 'user_group':
            usergroup = UserGroup.objects.get(id=id)
            widget = Widgets_trees.objects.get(id_widget=id_widget)
            Usergroup_permission.objects.update_or_create(
                usergroup=usergroup,
                widget=widget,
                defaults=dict(
                    permission=data
                ))
            return dict()

        return dict()


class Widgets_trees(AuditModel):
    def __str__(self):
        return self.id_widget

    id_widget = CodeField(unique=True)
    name = NameField()
    class_name = NameField()
    description = DescriptionField()
    structure = JSONField(default=dict)

    objects = Widgets_treesManager()

    def __str__(self):
        return f"id: {self.id_widget} name:{self.name_widget}, class_name:{self.class_name}"

    class Meta:
        verbose_name = 'Таблица сохранения деревьев виджетов объектов системы'
