Hello, ZERO
===========

Usage
-----

`pip install 0proto`

Then, simply use the command periodically:

`0proto https://example.com/something/etc`

This will save data to:

`settings.BASE_DIR/data/0proto-DOMAIN:default/Item`

N-Spacing
---------

If you want to seprate different sessions and sources, just use name param:

`0proto URI --name Name`

This will save to:
`settings.BASE_DIR/data/0proto-DOMAIN:Name/Type`

The `--name` value can be arbitray filesystem-compatible filename sub-string, so, you can use it to separate data by accounts, languages, or other features.

**NOTE**: Corresponding auth and session data will be stored in `settings.BASE_DIR/sessions` folder.

Saving to specific DIR
----------------------

Saving to custom folder simply pass `--path` parameter, like:

`0proto URI --name Name --path /home/mindey/Desktop/mydata`
