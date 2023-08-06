Hello, ONE
----------

Usage
-----

`pip install 1app`

Then, simply use the command periodically:

`1app --params...`

This will save data to:

`settings.BASE_DIR/data/1app:default/Item`

N-Spacing
---------

If you want to seprate different sessions and sources, just use name param:

`1app --params... --name Username`

This will save to:
`settings.BASE_DIR/data/1app:Name/Type`

The `--name` value can be arbitray filesystem-compatible filename sub-string, so, you can use it to separate data by accounts, languages, or other features.

**NOTE**: Corresponding auth and session data will be stored in `settings.BASE_DIR/sessions` folder.

Saving to specific DIR
----------------------

Saving to custom folder simply pass `--path` parameter, like:

`1app --params --name Name --path /home/mindey/Desktop/mydata`

