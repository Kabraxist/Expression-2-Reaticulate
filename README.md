# Expression-2-Reaticulate
## Info
A basic tool to convert Steinberg (Cubase / Nuendo / Dorico) Expression Maps (.expressionmap) to Reaper Reaticulate (.reabank) format.
The tool will export a Reaticulate-compatible .reabank file with some guesswork added for fancy visuals, based on [Spitfire UACC](https://spitfire-webassets.s3.amazonaws.com/pdfs/UACCv2spec.pdf).

Currently, only keyswitches supported. More switch styles (like MIDI CC) will be added in the future.

Any .expressionmap file should work. If not, please let me know!

## Usage
* Put the script files (_main.py and UACC List.csv_) beside a folder that includes .expressionmap files
* Run _main.py_. It will traverse the sibling folders, auto-convert .expressionmaps and move new files to a folder named "ReaBank Export"
* You can copy the contents of new files and use Reaticulate's "Paste from Clipboard" function

Please be aware that you still need to update some articulations by hand. 
Also, you might want to change "group" name (g="Converted Maps) field.

### Requirements
* Python 3.x
* untangle (pip install untangle)

## Support
Tested with Windows 10, Reaper v6.51, Reaticulate 0.5.6

Script is only tested in Windows environment, but should work in any Mac OS X or Linux distributions.

## Thanks to
Thanks [@jtackaberry](https://github.com/jtackaberry) for Reaticulate, which is an Virtual Instrument articulation manager extension for Reaper DAW
Check [Reaticulate](http://reaticulate.com/)!

Thanks [@dewdman42](https://github.com/dewdman42) for his extensive research on [ExpressionMap format](https://gitlab.com/dewdman42/emz/-/wikis/ExpressionMap-XML).
