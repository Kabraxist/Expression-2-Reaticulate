# Expression-2-Reaticulate
## Info
A basic tool to convert Steinberg (Cubase / Nuendo / Dorico) Expression Maps (.expressionmap) to Reaper Reaticulate (.reabank) format.
The tool will export a Reaticulate-compatible .reabank file with some guesswork added for fancy visuals, based on [Spitfire UACC](https://spitfire-webassets.s3.amazonaws.com/pdfs/UACCv2spec.pdf).

Currently, only keyswitches supported. More switch styles (like MIDI CC) will be added in the future.

Any .expressionmap file should work. If not, please let me know!

## Usage
* Put the script files (_main.py and UACC List.csv_) beside a folder that includes .expressionmap files
* Run the script. It will create a folder named "ReaBanks" which includes converted files
* You can copy the contents of new files and use Reaticulate's "Paste from Clipboard" function

### Requirements
* Python 3.x
* untangle (pip install untangle)

## Thanks to
Thanks [@jtackaberry](https://github.com/jtackaberry) for Reaticulate, which is an Virtual Instrument articulation manager extension for Reaper DAW
Check [Reaticulate](http://reaticulate.com/)!

Thanks [@dewdman42](https://github.com/dewdman42) for his extensive research on [ExpressionMap format](https://gitlab.com/dewdman42/emz/-/wikis/ExpressionMap-XML).
