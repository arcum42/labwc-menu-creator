import json
import pathlib
import xml.etree.cElementTree as ET

import desktop_entry

categories = {}

cat_path = pathlib.Path(__file__).parent / "categories.json"
with cat_path.open("r") as f:
    categories = json.load(f)

desktop_entries = desktop_entry.get_desktop_entries()

app_list = []
for entry in desktop_entries:
    app = desktop_entry.parse_desktop_entry(entry)
    if app:
        if "only_show_in" not in app and "not_show_in" not in app:
            if "NoDisplay" not in app and "Hidden" not in app:
                if "terminal" not in app or app["terminal"] == "false":
                    temp = []
                    for item in app['categories']:
                        if item in categories['mapping']:
                            temp.append(categories['mapping'][item])
                        else:
                            temp.append(item)
                    app['categories'] = temp
                    app_list.append(app)

app_list = sorted(app_list, key=lambda x: x['name'])

menu = {}
menu['Steam'] = []

for j,entry in enumerate(app_list):
    if 'exec' in entry:
        for exe in categories['by-exec']:
            if exe in entry['exec']:
                entry['categories'] = [categories['by-exec'][exe]]

    if 'name' in entry:
        for name in categories['by-name']:
            if name in entry['name']:
                entry['categories'] = [categories['by-name'][name]]


    for item in categories['exclusive']:
        if item in entry['categories']:
            entry['categories'] = [item]

    for i, category in enumerate(entry['categories']):
        blacklisted = False
        for item in categories['blacklist']:
            if item in category:
                blacklisted = True

        if blacklisted:
            continue

        if category in categories['mapping']:
            category = categories['mapping'][category]
            app_list[j]['categories'][i] = category

        if category not in menu:
            menu[category] = []

        if entry not in menu[category]:
            menu[category].append(entry)

root = ET.Element("openbox_pipe_menu")

for category in categories['main']:
    ET.SubElement(root, "menu", label=category, id=category, icon=categories['icons'].get(category, "applications-other"))

for entry in menu:
    if entry in categories['subcategory']:
        search = f"./menu[@label='{categories['subcategory'][entry]}']"
        cat = ET.SubElement(root.find(search), "menu", label=entry, id=entry, icon=categories['icons'].get(entry, "applications-other"))
    elif entry not in categories['main']:
        cat = ET.SubElement(root.find("./menu[@label='Other']"), "menu", label=entry, id=entry, icon=categories['icons'].get(entry, "applications-other"))
    else:
        cat = root.find(f"./menu[@label='{entry}']")

    for app in menu[entry]:
        entry = None
        if 'icon' not in app:
            entry = ET.SubElement(cat, "item", label=app['name'])
        else:
            entry = ET.SubElement(cat, "item", label=app['name'], icon=app['icon'])
        action = ET.SubElement(entry, "action", name="Execute")
        command = ET.SubElement(action, "command")
        command.text = app['exec']
ET.indent(root)
print(ET.tostring(root).decode())

with cat_path.open("w") as f:
    json.dump(categories, f, indent=4)
