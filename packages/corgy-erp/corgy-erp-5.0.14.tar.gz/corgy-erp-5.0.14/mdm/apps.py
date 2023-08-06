from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class MdmConfig(ModuleMixin, AppConfig):
    name = 'mdm'
    icon = '<i class="material-icons">settings_applications</i>'
