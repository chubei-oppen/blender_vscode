import bpy
from bpy.props import *
from . package_installation import is_pip_installed, is_package_installed
from . ptvsd_server import get_active_ptvsd_port, ptvsd_debugger_is_attached

class MyPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    package_name_to_install: StringProperty("Package Name to Install")
    addon_to_reload: StringProperty("Addon to Reload")

    def draw(self, context):
        layout: bpy.types.UILayout = self.layout
        if not is_pip_installed():
            layout.operator("development.install_pip")
        else:
            row = layout.row(align=True)
            row.prop(self, "package_name_to_install", text="Install Package")
            props = row.operator("development.install_python_package", text="", icon='IMPORT')
            props.package_name = self.package_name_to_install

            if not is_package_installed("ptvsd"):
                props = layout.operator("development.install_python_package", text="Install ptvsd (Python Debugger)")
                props.package_name = "ptvsd"

        if is_package_installed("ptvsd"):
            ptvsd_port = get_active_ptvsd_port()
            if ptvsd_port is None:
                layout.operator("development.start_ptvsd_server")
            else:
                layout.label(text=f"ptvsd is running at port {ptvsd_port}")
                if ptvsd_debugger_is_attached():
                    layout.label(text="Debugger is attached")

        row = layout.row(align=True)
        row.prop(self, "addon_to_reload", text="Reload Addon")
        props = row.operator("development.reload_addon", text="", icon='FILE_REFRESH')
        props.module_name = self.addon_to_reload
