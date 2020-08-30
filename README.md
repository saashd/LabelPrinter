# LabelPrinter
Prog that allows to print on label printer (like brother ql-700), in remote control.
The prog uses tamplate of the label (png file).


You should `pip install brother_ql`, `pip install pyusb` and  install `libusb-win32\bin`.
In cmd: type `ipconfig` to check your IP adress, in case you want to run the prog not as a local host.

### Config file (`config.json`):
```javascript
{
    "port" : int, (port number to listen to)
    "localhost" : bool (whether to run on localhost)
}
```


How to parse `.py` to `.exe`:
 Install `pyinstaller` and write in cmd: `pyinstaller --onefile "pyhton_file_name".py`

