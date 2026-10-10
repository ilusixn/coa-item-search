# CoA Item Search

A World of Warcraft 3.3.5a addon for **Conquest of Azeroth** private servers (AzerothCore CoA, CoA Server Manager,
CoA Custom). It searches every item of the server by name or ID and adds the item to your bags with one click.

* `/items` (or `/itemsearch`) opens the window. `/items thunderfury` searches right away.
* Type a name, part of a name or an item ID, then press **Enter**.
* Each result shows its icon, its name in quality colour, its ID and its item level.
* **Add item** sends `.additem <id> <count>`. Set the count in the **Count** box. Your account needs GM rights on
  the server (game master or administrator).
* Hover a row for the item tooltip. Shift-click a row to link the item in chat. Escape closes the window, and it can
  be dragged.

## Install

1. Copy `CoAItemSearch` and `CoAItemSearch_Data` into your client's `Interface\AddOns` folder.
2. Restart the game: `/reload` does not find new addons.
3. At character select, open **AddOns** and make sure both are ticked.

`CoAItemSearch_Data` is the item list. It loads only the first time you open the window, so it costs no memory
until you use it.

## Item list for your own server

Every server has its own items, so the list is generated from its database:

```
python tools/make_item_data.py --mysql "C:/CoA-Repack/mysql/bin/mysql.exe" --defaults "C:/CoA-Repack/mysql/admin-client.ini"
```

That writes `CoAItemSearch_Data/data1.lua` to `data8.lua`. The release zip includes a prebuilt list from a
CoA Custom 1.5 server (568,379 items).

## Credits

Made for CoA Custom by ilusixn. Conquest of Azeroth server core by jealous-sound, and CoA Server Manager by Corfirean.
