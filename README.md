## Setup

### Installation

Extract this repo to a directory of your choice, open powershell/cmd in that directory.

OPTIONAL: Setup a python virtual environment: `py -m venv venv`

OPTIONAL: Enable the virtual environment:
- Windows: `venv/scripts/activate`
- Linux: `source venv/bin/activate`

Install requirements: `pip install -r requirements.txt`
If not using a virtual environment, use pip3 instead of pip.

Visit the [PyTorch website](https://pytorch.org/) and generate the correct command for your system.
For Package hit "Pip", for Language hit "Python".
If you are using a modern Nvidia card with up-to-date drivers select the latest CUDA for Compute Platform.
If using AMD or no GPU at all, hit CPU instead.
Copy the command generated (change pip3 to pip if using virtual environment), run it in terminal, installation complete!

### Configuration

Edit this file appropriately:
-   `bot_token` is the client token of your Discord bot.
-   `bot_prefix` is the prefix that will be used on all the bot's commands.
-   `img_size_cutoff` is the maximum resolution that you will allow someone to submit to the bot to avoid extended upscaling times.
-   `moderator_role_id` is the role id (can also be the name of the role) that will be allowed to run certain restricted commands.
-   `global_guild_block`, keep this false if you want the bot to be able to run in any server.
