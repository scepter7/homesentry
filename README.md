# homesentry
Automated surveillance system written in Python with usage of OpenCV.

## How it works
System consists of separate server and surveillance system, which consists of several modules, such as camera module, motion detection module, etc.
Control of the surveillance system is performed via sending requests to the server.
Requests are sent via Telegram bot mentioned above.
Server sends frames with captured movement to the bot for user to see.

This software is supposed to be used with [Telegram bot](https://github.com/eliasxyz/pytelebot).

## Requirements
Requirements are listed in `requirements.txt` file. Install them with `pip install -r requirements.txt`.

**Warning! Some systems, such as Raspberry Pi require manual OpenCV compilation, installing it with pip will fail!**

To function you have to have camera device connected.

## Usage
Run `python main.py`. This will run a server, which awaits commands from user.
Usage and configuration of Telegram bot is described [here](https://github.com/eliasxyz/pytelebot).

Configuration is performed via editing `config.json` file:
* `camera_warmup` - int, time in seconds for camera sensor to warm up before being used;
* `delta_thresh` - int, the minimum absolute value difference between current frame and averaged frame for a given pixel to be triggered as motion. Small values cause more motion to be detected, larger values - less motion;
* `min_area` - int, the minimum size of an object to be considered as moveable, small values cause more motion detection, larger values - less detection, only on large objects;
* `is_streaming` - bool, allows to display camera videofeed, if hardware has available displays to show it;
* `url` - system configuration, used for creating queries to Telegram bot.

## Examples
![Sent Frame](examples/2.jpg?raw=true "Sent_Frame")
This is an example of the frame, which user gets via Telegram bot. System captured possible intruder, moveable object is highlighted with rectangle, date and time of detection is displayed on the bottom of the frame.

