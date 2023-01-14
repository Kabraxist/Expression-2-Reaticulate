# Expression-2-Reaticulate
## Info
This tool converts Steinberg (Cubase / Nuendo / Dorico) Expression Maps (.expressionmap) and Apple Logic Articulation Maps (.plist) to Reaper Reaticulate (.reabank) format. It will export a Reaticulate-compatible .reabank file, with some visual enhancements based on [Spitfire UACC](https://spitfire-webassets.s3.amazonaws.com/pdfs/UACCv2spec.pdf) list.

Currently, only keyswitches and CC messages are supported.

## Usage
* Download the archive file
* Export files beside the folder that includes .expressionmap or .plist files
* Run _main.py_
* The script will scan sibling folders, convert maps, then move new files to "ReaBank Export".
* You can copy the text from new documents and use Reaticulate's "Paste from Clipboard" feature to add them to your project.
* You might want to change "group" name (g="Converted Maps) field.

## Support
Tested with Windows 10, Reaper v6.51, Reaticulate 0.5.6

Script is only tested in Windows environment, but should work in any Mac OS X or Linux distributions.

## Thanks to
Thanks [@jtackaberry](https://github.com/jtackaberry) for Reaticulate, which is an Virtual Instrument articulation manager extension for Reaper DAW
Check [Reaticulate](http://reaticulate.com/)!

Thanks [@dewdman42](https://github.com/dewdman42) for his extensive research on [ExpressionMap format](https://gitlab.com/dewdman42/emz/-/wikis/ExpressionMap-XML).
