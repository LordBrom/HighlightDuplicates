'''
Provides duplicated lines highlighter.

Config summary (see README.md for details):

    # file settings
    {
      "highlight_duplicates_color": "invalid"
    }

@author: Nate Mills <mills.nate@gmail.com>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2017-10-17

@author: Aurelien Scoubeau <aurelien.scoubeau@gmail.com>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2012-09-26
'''
# inspired by https://github.com/SublimeText/TrailingSpaces
import sublime
import sublime_plugin
from collections import defaultdict

DEFAULT_COLOR_SCOPE_NAME = "invalid"
DEFAULT_IS_ENABLED = True
DEFAULT_IS_DISABLED = False
DEFAULT_MIN_LINE_LENGTH = 4
DEFAULT_MIN_DUPLICATE_COUNT = 1

def count_lines(lines, view):
    '''Counts line occurrences of a view using a hash.
    The lines are stripped and tested before count.
    '''
    counts = defaultdict(list)
    for line in lines:
        string = view.substr(line)
        if trimWhiteSpace():
            string = string.strip()
        if ignoreCase():
            string = string.lower()
        if is_candidate(string):
            counts[string].append(line)
    return counts


def filter_counts(counts):
    '''Filters the line counts by rejecting every line having a count
    lower or equal to the "min_duplicate_count" user setting, which defaults to 1.
    '''
    filtered = dict()
    threshold = getMinDuplicateCount();
    for k, v in counts.items():
        if len(v) > threshold:
            filtered[k] = v
    return filtered


def remove_first(counts):
    '''Removes the first region of each duplicate line
    '''
    trimmed = dict()
    for k, v in counts.items():
        v.pop(0)
        trimmed[k] = v
    return trimmed


def merge_results(countsList):
    '''Merges the individual region lists
    into one list
    '''
    merged = []
    for k in countsList:
        for v in k:
            merged.append(v)
    return merged


def is_candidate(string):
    '''Tells if a string is a LOC candidate.
    A candidate is a string long enough after stripping some symbols.
    '''
    minLineLength = getMinLineLength()
    ignoreList = getIgnoreList()
    if len(ignoreList) > 0 and string.strip().lower() in ignoreList:
        return False
    return len(string.strip('{}()[]/')) >= minLineLength


def show_lines(regions, view):
    '''Merges all duplicated regions in one set and highlights them.'''
    all_regions = []
    for r in regions:
        all_regions.extend(r)
    color_scope_name = getHighlightColor()
    view.add_regions('DuplicatesHighlightListener',
                        all_regions, color_scope_name, '',
                        sublime.DRAW_OUTLINED)


def add_lines(regions, view):
    '''Merges all duplicated regions in one set and highlights them.'''
    view.sel().clear()
    for r in regions:
        for i in r:
            view.sel().add(i)


def remove_lines(regions, view, edit):
    for r in reversed(regions):
        view.erase(edit, sublime.Region(r.begin()-1, r.end()))


def highlight_duplicates(view):
    '''Main function that glues everything for hightlighting.'''
    # get all lines
    lines = view.lines(sublime.Region(0, view.size()))
    # count and filter out non duplicated lines
    duplicates = filter_counts(count_lines(lines, view))
    # show duplicated lines
    show_lines(duplicates.values(), view)



def select_duplicates(view):
    '''Main function that glues everything for hightlighting.'''
    # get all lines
    lines = view.lines(sublime.Region(0, view.size()))
    # count and filter out non duplicated lines
    duplicates = filter_counts(count_lines(lines, view))
    # select duplicated lines
    add_lines(duplicates.values(), view)



def remove_duplicates(view, edit):
    '''Main function that glues everything for hightlighting.'''
    # get all lines
    lines = view.lines(sublime.Region(0, view.size()))
    # count and filter out non duplicated lines
    duplicates = remove_first(filter_counts(count_lines(lines, view)))
    # select duplicated lines
    merged = merge_results(duplicates.values())
    merged.sort(key=lambda elm: elm.begin())
    remove_lines(merged, view, edit)


def downlight_duplicates(view):
    '''Removes any region highlighted by this plugin accross all views.'''
    view.erase_regions('DuplicatesHighlightListener')

def update_settings(newSetting):
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    settings.set('highlight_duplicates_enabled', newSetting)
    sublime.save_settings('highlight_duplicates.sublime-settings')

def isEnabled():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    return bool(settings.get('highlight_duplicates_enabled', DEFAULT_IS_ENABLED))

def trimWhiteSpace():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    return bool(settings.get('trim_white_space', DEFAULT_IS_ENABLED))

def ignoreCase():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    return bool(settings.get('ignore_case', DEFAULT_IS_DISABLED))

def getHighlightColor():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    return settings.get('highlight_duplicates_color', DEFAULT_COLOR_SCOPE_NAME)

def getMinLineLength():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    minLength = settings.get('min_line_length', DEFAULT_MIN_LINE_LENGTH)
    if isinstance(minLength, int):
        return minLength
    else:
        return DEFAULT_MIN_LINE_LENGTH

def getMinDuplicateCount():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    minLength = settings.get('min_duplicate_count', DEFAULT_MIN_DUPLICATE_COUNT)
    if isinstance(minLength, int):
        return max(DEFAULT_MIN_DUPLICATE_COUNT, minLength)
    else:
        return DEFAULT_MIN_DUPLICATE_COUNT

def getIgnoreList():
    settings = sublime.load_settings('highlight_duplicates.sublime-settings')
    ignoreList = settings.get('ignore_list', [])
    for i in range(len(ignoreList)):
        ignoreList[i] = ignoreList[i].strip().lower()

    return ignoreList



class HighlightDuplicatesCommand(sublime_plugin.WindowCommand):
    '''Actual Sublime command. Run it in the console with:
    view.window().run_command('highlight_duplicates')
    '''
    def run(self):
        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if isEnabled():
            highlight_duplicates(self.window.active_view())
        else:
            downlight_duplicates(self.window)


class DuplicatesHighlightListener(sublime_plugin.EventListener):
    '''Handles sone events to automatically run the command.'''
    def on_modified(self, view):
        if isEnabled():
            highlight_duplicates(view)
        else:
            downlight_duplicates(view)

    def on_activated(self, view):
        if isEnabled():
            highlight_duplicates(view)
        else:
            downlight_duplicates(view)

    def on_load(self, view):
        if isEnabled():
            highlight_duplicates(view)
        else:
            downlight_duplicates(view)


class ToggleHighlightDuplicatesCommand(sublime_plugin.WindowCommand):
    def run(self):

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if isEnabled():
            update_settings(False)
            downlight_duplicates(self.window.active_view())
        else:
            update_settings(True)
            highlight_duplicates(self.window.active_view())


class ToggleSelectDuplicatesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        select_duplicates(self.view)
        self.view.end_edit(edit)


class RemoveDuplicatesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        remove_duplicates(self.view, edit)
