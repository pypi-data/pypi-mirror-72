# pyhypixel

This is an unofficial Python3 [HypixelAPI](https://github.com/HypixelDev/PublicAPI) wrapper.

## Installation

You can simply install the package by using:

`python3 -m pip install pyhypixel`

## Usage

First of all you have to get an api key by using `/api` while on Hypixel network.

Everything starts with the creation of an api instance:

```python
from hypixelapi import hypixelapi


api = hypixelapi.HypixelAPI('YOUR_HYPIXEL_API_KEY')
```

You can get a player by using:

```python
player = api.get_player('SonoMichele') # also works with uuid
```

You can get a guild by using one of three methods:

```python
# first method using guild id
guild_by_id = api.get_guild_by_id('52e57a1c0cf2e250d1cd00f8')

# second method using guild name
guild_by_name = api.get_guild_by_name('The Sloths')

# third method using a player instance
guild_by_player = player.get_guild()
```

## Documentation

A detailed documentation is available [here](https://github.com/xMicky24GIT/pyhypixel/blob/master/DOCUMENTATION.md)

## Contributing

If you want to contribute you can do it by opening an [issue](https://github.com/xMicky24GIT/pyhypixel/issues) or a [pull request](https://github.com/xMicky24GIT/pyhypixel/pulls).

You can also contact me on telegram [@sonomichelequellostrano](https://t.me/sonomichelequellostrano)

All contributors will be listed on this repository.
