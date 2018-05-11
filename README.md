dolores.py
==========

A stupid little script to control your Ecovacs Deebot robot vacuum with Westworld host commands.

Usage
-----

1. Install dependencies using `pipenv`
2. Create a login configuration file at `~/.config/sucks.conf` using the [sucks](https://github.com/wpietri/sucks) `login` command, or manually. It will look something like this:

```
email=you@example.com
password_hash=MD5_HASH_OF_PASSWORD
device_id=MD5_HASH_OF_ANYTHING
country=us
continent=na
```

3. Run `python dolores.py`
4. Brace yourself for the uprising

Credits
-------

1. `sucks`: https://github.com/wpietri/sucks
2. `Pocketsphinx`: https://github.com/bambocher/pocketsphinx-python

License
-------

Copyright (C) 2018 Tom Robinson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
