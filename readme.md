# Highlight Duplicates

**Highlight duplicated lines.**
This is a [Sublime Text 3](http://www.sublimetext.com/3) plugin.


## Installation

Go to your `Packages` subdirectory under ST3's data directory:

* Windows: `%APPDATA%\Sublime Text 3`
* OS X: `~/Library/Application Support/Sublime Text 3/Packages`
* Linux: `~/.config/sublime-text-3`
* Portable Installation: `Sublime Text 3/Data`

Then clone this repository:

    git clone git://github.com/lordbrom/HighlightDuplicates.git

That's it!


## Options

Some options are available to customize the plugin look 'n feel. The
config keys goes into config files accessible throught the "Preferences"
menu.

### Change the highlighting color

The highlighting color can be changed by providing a scope name such
as "invalid", "comment"... in "File Settings - User":

``` js
{ "highlight_duplicates_color": "invalid" }
```

"invalid" is the default value. If you'd like to use a custom color,
it should be defined as a color scope in your theme file.


### Enable or disable the plugin

If needed, you can enable or disable the plugin with the following option:
```js
{ "highlight_duplicates_enabled" : true }
// or
{ "highlight_duplicates_enabled" : false }
```


## Run it

As soon as it's installed, it's working. Then, you can toggle the highlighting with `Tools > Command Palette` (command + shift + p on OSX) and start typing `duplicates`. Select the command in the list and hit enter.
