# Highlight Duplicates

**Highlight duplicated lines.**
This is a [Sublime Text 3](http://www.sublimetext.com/3) (and ST2) plugin.


## Installation

**Using Package Control** ([installation instructions](https://packagecontrol.io/installation))

Press ctrl+shift+p (cmd+shift+p for OSX), then use the 'Package Control: Install Package' command.  
Search for 'HighlightDuplicates', and press enter to install.


**Manually**

Go to your `Packages` subdirectory under ST3's data directory:

* Windows: `%APPDATA%\Sublime Text 3`
* OS X: `~/Library/Application Support/Sublime Text 3/Packages`
* Linux: `~/.config/sublime-text-3`
* Portable Installation: `Sublime Text 3/Data`

Then clone this repository:

    git clone git://github.com/lordbrom/HighlightDuplicates.git


That's it!


## Commands

### Toggle Highlighting 

Using this command will turn the plugin on and off. Allowing you to only see the highlighted duplicates when you want, without having to disable/enable to plugin via the Package Control.


### Select Duplicates

Using this command will select the rows that would be highlighted when Highlight Duplicates is toggled on. The duplicate rows do not need to be highlighted in order for this command to work.


_Note:_ By default neither of these commands have a key binding, and can only be used via the Command Palette. You can set a key binding by adding one, or both of the following lines to the key binding file. (Preferences > Key Bindings) 

``` js
{ "keys": ["alt+shift+h"], "command": "toggle_highlight_duplicates" }
{ "keys": ["alt+shift+s"], "command": "toggle_select_duplicates" }
```

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


### Trim white space

If this setting is true, the leading and trailing whitespace will be removed before being compared to other lines. This setting also affects which lines are selected when using the 'Select Duplicates' command.

For example, if `"trim_white_space" : true` the following 2 lines will be counted as duplicates.  
``` html
1: <someTag></someTag>
2:      <someTag></someTag>
```  
However, these lines would not, since there is white space in line 1, that is not leading or trailing  whitespace, which is not in line 2.  
``` html
1: <someTag>      </someTag>
2:      <someTag></someTag>
```


### Ignore Case

If this setting is true, upper and lower case letters will be concidered the same. This setting also affects which lines are selected when using the 'Select Duplicates' command.

For example, if `"ignore_case" : true` the following 2 lines will be counted as duplicates.
``` html
1: <SomeTag></sOMeTag>
2: <sometag></someTag>
```
