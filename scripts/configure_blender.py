"""Configure the installed official MCP extension for local use."""
import bpy

prefs = bpy.context.preferences
prefs.system.use_online_access = True
prefs.view.show_splash = False
addon = prefs.addons["bl_ext.user_default.mcp"].preferences
addon.host = "127.0.0.1"
addon.port = 9876
addon.use_autostart = True
bpy.ops.wm.save_userpref()
print("Official Blender MCP configured on 127.0.0.1:9876")
