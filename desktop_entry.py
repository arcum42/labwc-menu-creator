import os
import pathlib
from configparser import ConfigParser

def get_data_dirs():
    dir_list = []

    if "XDG_DATA_HOME" in os.environ:
        dir_list.append(os.environ["XDG_DATA_HOME"])

    if "HOME" in os.environ:
        dir_list.append(os.environ["HOME"] + "/.local/share")

    if "XDG_DATA_DIRS" in os.environ:
        data_dirs = os.environ["XDG_DATA_DIRS"].split(":")
        for d in data_dirs:
            dir_list.append(d)

    dir_list.append("/usr/local/share")
    dir_list.append("/usr/share")
    dir_list.append("/opt/share")

    dir_list = list(set(dir_list)) # Remove duplicates

    return dir_list

def get_desktop_entries():
    desktop_entries = []

    dir_list = get_data_dirs()
    for d in dir_list:
        cur = pathlib.Path(d)
        if cur.exists():
            desktop_entries.extend(list(cur.glob("*.desktop")))
            desktop_entries.extend(list(cur.glob("applications/*.desktop")))
            desktop_entries.extend(list(cur.glob("desktop-directories/*.desktop")))

    desktop_entries = list(set(desktop_entries))

    return desktop_entries

def parse_desktop_entry(path):
    config = ConfigParser(interpolation=None)
    config.read(path)

    desktop_entry = {}

    if "Desktop Entry" in config:
        entry = config["Desktop Entry"]
        desktop_entry['full_path'] = path

        if "Name" in entry:
            desktop_entry['name'] = entry["Name"]
        else:
            desktop_entry['name'] = path.stem

        if "Categories" in entry:
            categories = entry["Categories"].split(";")
            categories = list(filter(None, categories))
            categories = list(map(lambda x: x.strip(), categories))
            desktop_entry['categories'] = categories
        else:
            desktop_entry['categories'] = []

        if "Exec" in entry:
            desktop_entry['exec'] = entry["Exec"]

        if "Icon" in entry:
            desktop_entry['icon'] = entry["Icon"]

        if "Type" in entry:
            desktop_entry['type'] = entry["Type"]

        if "Terminal" in entry:
            desktop_entry['terminal'] = entry["Terminal"]

        if "NoDisplay" in entry:
            desktop_entry['no_display'] = entry["NoDisplay"]

        if "Hidden" in entry:
            desktop_entry['hidden'] = entry["Hidden"]

        if "OnlyShowIn" in entry:
            desktop_entry['only_show_in'] = entry["OnlyShowIn"]

        if "NotShowIn" in entry:
            desktop_entry['not_show_in'] = entry["NotShowIn"]

        if "MimeType" in entry:
            desktop_entry['mime_type'] = entry["MimeType"]

        if "Keywords" in entry:
            keywords = entry["Keywords"].split(";")
            keywords = list(filter(None, keywords))
            keywords = list(map(lambda x: x.strip(), keywords))
            desktop_entry['keywords'] = keywords

        if "StartupNotify" in entry:
            desktop_entry['startup_notify'] = entry["StartupNotify"]

        if "StartupWMClass" in entry:
            desktop_entry['startup_wm_class'] = entry["StartupWMClass"]

        if "URL" in entry:
            desktop_entry['url'] = entry["URL"]

        if "Path" in entry:
            desktop_entry['path'] = entry["Path"]

        if "Actions" in entry:
            actions = entry["Actions"].split(";")
            actions = list(filter(None, actions))
            actions = list(map(lambda x: x.strip(), actions))
            desktop_entry['actions'] = actions

        if "DBusActivatable" in entry:
            desktop_entry['dbus_activatable'] = entry["DBusActivatable"]

        if "TryExec" in entry:
            desktop_entry['try_exec'] = entry["TryExec"]

        if "GenericName" in entry:
            desktop_entry['generic_name'] = entry["GenericName"]

        if "Comment" in entry:
            desktop_entry['comment'] = entry["Comment"]

        return (desktop_entry)
    return None
