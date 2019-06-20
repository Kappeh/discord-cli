# discord-cli

A simple command system builder for discord bots. Parses, validates and authenticates commands to be executed by your discord bots.

## Getting Started

Before you get started, you will need python3 and the discord py package.

### Virtual Environment
It is recommended that you install your packages within a virtual environment. This is an optional step, however. To create and activate your virtual environment, run the following commands
```
python3 -m venv venv
source venv/bin/activate
```

Now all pip packages that you install will only exist within this environment. You can activate it whenever you wish by activating the second command within the same directory.

### Discord Py Package
The discord py package can be installed using the following command
```
python3 -m pip install discord
```

### Installing

To install the discord-cli package simply run
```
python3 -m pip install discord-cli
```

If the install is successful, you should be able execute the following
```
python3
> import discord_cli
> discord_cli.__name__
```
and get an output of
```
'discord-cli'
```

## Basic Usage

### Simple Command System Example

Let's say we wish to achieve the following command tree with two commands: add and subtract - each taking in two floats as arguments: left and right.
```
+ MyCommandSystem
|
+ - + add
|     Arguments:
|       left:float
|       right:float
|
+ - + subtract
      Arguments:
        left:float
        right:float
```

We can write the following code
```py
# Importing the module
import discord_cli as dcli

# Creating the command system
cs = dcli.Command_System('MyCommandSystem')

# The code that is run when the command is invoked
# The parameters should always be the same.
async def add_func(client, message, params, *argv, **kwargs):
    return str(params['left'] + params['right'])
# Creating the command
add_cmd = cs.command('add', function = add_func)
# Adding the arguments to the command
add_cmd.argument.float('left')
add_cmd.argument.float('right')

# This is repeated for the subtraction command
async def subtract_func(client, message, params, *argv, **kwargs):
    return str(params['left'] - params['right'])
subtract_cmd = cs.command('subtract', function = subtract_func)
subtract_cmd.argument.float('left')
subtract_cmd.argument.float('right')
```

To see if everything has correctly been organised, we can use the following line of script:
```py
print(cs.tree_string(details = True))
```

If everything has worked properly, the command tree from above should be printed to your console.

### Using The Command System With A Discord Bot

In order to run a bot with this command system, there is a little more work to be done. At the top of your file, import the discord module.
```py
import discord
```

After you have created the command system, append the following code.
```py
CLIENT = discord.Client()
TOKEN = 'REPLACE_THIS_WITH_YOUR_SECRET_DISCORD_BOT_TOKEN'
PREFIX = '!'

@CLIENT.event
async def on_message(message):
    if message.author.id == CLIENT.user.id:
        return
    if not message.content.startswith(PREFIX):
        return

    command = message.content[1:]
    result = await cs.execute(CLIENT, message, command)

    if isinstance(result, str):
        await message.channel.send(result)
    if isinstance(result, discord.Embed):
        await message.channel.send(embed = result)

CLIENT.run(TOKEN)
```

If you're having trouble creating a discord bot account or finding your secret token, you can find more information [here](https://github.com/SinisterRectus/Discordia/wiki/Setting-up-a-Discord-application).

To further customize your discord bot, you can read up on the discord py package [here](https://discordpy.readthedocs.io/en/latest/api.html).

## Documentation

A more detailed documentation can be found [here](https://kappeh.github.io/discord-cli).

## Contributing

The code of conduct for contributing is currently unavailable.

## Authors

* **Kieran Powell** - *Initial work* - [Kappeh on Github](https://github.com/Kappeh)

See also the list of [contributors](https://github.com/Kappeh/discord-cli/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.