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

Using this command will turn the plugin on and off. This allows you to see the highlighted only when you want without having to disable/enable to plugin via the Package Control.


### Select Duplicates

Using this command will select the rows that would be highlighted when Highlight Duplicates is toggled on. The duplicate rows do not need to be highlighted in order for this command to work.


### Remove Duplicates

Using this command will remove all duplicate lines from the file. The first instance of each duplicate will be kept. This command is similar to the build in "Permute Lines > Unique" function found in the Edit menu, however with this you are able to ignore letter case. 

For example...
``` html
1: <someTag></someTag>
2: Content
3: <someTag></someTag>
4: 
```  
Would result in
``` html
1: <someTag></someTag>
2: Content
3: 
```


_Note:_ By default none of these commands have a key binding, and can only be used via the Command Palette. You can set a key binding by adding one, or both, of the following lines to the key binding file. (Preferences > Key Bindings) 

``` js
{ "keys": ["alt+shift+h"], "command": "toggle_highlight_duplicates" }
{ "keys": ["alt+shift+s"], "command": "toggle_select_duplicates" }
{ "keys": ["alt+shift+r"], "command": "remove_duplicates" }
```

## Options

### Change The Highlighting Color  
`Default: "invalid"`

The highlighting color can be changed by providing a scope name such
as "invalid", "comment", etc...

If you'd like to use a custom color,
it should be defined as a color scope in your theme file.


### Trim White Space  
`Default: true`

If this setting is true, the leading and trailing white space will be removed before being compared to other lines. This setting also affects which lines are selected when using the 'Select Duplicates' command.

For example, if `"trim_white_space" : true` the following 2 lines will be counted as duplicates.  
``` html
1: <someTag></someTag>
2:      <someTag></someTag>
```  
However, the following lines would not be counted as duplicates. The reason for this is because there is white space in line 1 that is not leading or trailing, which does not appear in line 2. 
``` html
1: <someTag>      </someTag>
2:      <someTag></someTag>
```


### Ignore Case  
`Default: false`

If this setting is true, upper and lower case letters will be considered the same. This setting also affects which lines are selected when using the 'Select Duplicates' command.

For example, if `"ignore_case" : true` the following 2 lines will be counted as duplicates.  
``` html
1: <SomeTag></sOMeTag>
2: <sometag></someTag>
```
