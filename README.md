# Waypointer
*Waypointer, a simple way to plot multiple locations from drone flight logs.* :rocket:

### Overview
This software is a couple of python scripts that should (with the right files) extract longitude
and latitude from the said file. Then after some sorting of the relevant data feed it into
a google maps api and plot all the waypoints from a certain sequence (flighing session) as well as 
relevant meta data.

#### Supported Drones
* DJI Phantom 2 (Ground station app sqlite database file)
* DJI Phantom 3 (CSV file from DatCon output)
* Parrot Bebop 2 (PUD file from either mobile device used for flight or drone itself)

---

### Installation
Once you have a copy of this directory then you'll want to do the following in your terminal.

`cd [your/directory/Waypointer]`

`chmod +x INSTALL.sh`

`sudo ./INSTALL.sh`

You'll then need to input your password for your system.

If prompted accept you want to download relevant software by tpying `y` and hitting enter/return.

---

### Usage
#### Parameters
Be within the Waypointer folder.

`python waypointer.pyc [sequence number] [sqlite database file]` for 'GroundStation' app.

`python bebop.pyc [pud file]` for Parrot Bebop 2 files saved as pud files.

This all gets a lot simpler if you copy the file into the 'Waypointer' folder, wherever that may be on 
your system. Failing that you can just type the full address of where it is such as `~/Downloads/.../database.sqlite`

#### Result
The result of this should be that you get a .html file by the name of sequence[value you chose].html, or [pud filename].html. Within the
Waypointer folder. The file will also be automatically opened but it is saved within Waypointer should you want to open
it at a later date, send it to someone else or whatever your heart desires. You can always generate the original again.

Finally, meta data should be have also been gained from the files used and then displayed on the right hand side of the web page.

---

### Side note
* It's worth noting that the source code should be in the folder should you want to edit it and hopefully commented thourougly 
enough for your needs.
* 'simplemap' is not my creation, credit goes to user 'patrick--' on github, it uses the MIT license.
* `pud_to_csv_kml.py` is not my creation, credit goes to user 'matthewlloyd' on github, this one has no license.
* Part of the process with the `bebop.py` script is it also creates a csv file if you wanted to look at data excluding meta.
* If you're generating lots of flying sessions and not familiar with terminal. Use the up arrow to cycle through previously 
executed commands.
* `config.json` has an api key within it. Should you need to change it for whatever reason you replace it by generating your own
on [Googles developer site.](https://developers.google.com/maps/documentation/javascript/get-api-key)
* Sometimes in the terminal it seems to 'hang' when the .html file has been opened. Feel free to `Ctrl+C` in the terminal, it's just
an idiosyncrasy of the python module `webbrowser` as far as I can tell.

---
