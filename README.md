labwc-menu-creator is a tool for creating a menu for labwc, specifically generating a pipe menu, not the entire menu. It is designed to be used with labwc, but could likely be used with openbox or any other window manager that supports pipe menus.

This is also mostly a personal project at the moment, and isn't going to be particularly easy to use right now. It is still in development and may have bugs or missing features. Please report any issues or feature requests on the GitHub repository.

## Usage

Currently, it relies on being run from whereever you've placed it on your system, as it looks for the categories.json file in that directory.

If, for example, you had it in your home directory, you could add the following line to your menu.xml file:
```  <menu id="root-menu" label="" execute="python ~/labwc-menu-creator/labwc-menu-creator.py" />```

As it just prints the menu to stdout, you can redirect it to a file or pipe it to another command.

No command line arguments are currently supported, but this may change in the future.

The categories.json file can be customized to change the structure of the generated menu. It has the following sections:
icons: This section is a dictionary with the keys being category names, and the values being icon names.
main: The main categories in the main menu. All others will be placed in a submenu of 'Other'.
mapping: Any of these categories will be changed to the specified category instead.
subcategory: This specifies which category a subcategory belongs to, rather than the default 'Other'.
blacklist: Any of these categories are skipped.
by-exec: This places a program in a category based on the executable string given. The string given just needs to be contained within the executable string, not the full string.
by-name: Similar to by-exec, but based on the name of the program.
exclusive: Any programs in these categories will not be included in any other category.

This is all subject to change, and is largely just what I added to get the menu looking the way I wanted it to. For example, I wanted all steam games in their own category. I may still modify this, as currently, the list of steam games still is longer then the size of my window.

Feel free to submit a pull request if you have any changes you'd like to see, though there's no guarantee that it will be accepted. Anything to make the program more easier to use is welcome, as long as the changes don't break the existing functionality.
