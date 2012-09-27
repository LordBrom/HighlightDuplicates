'''
Provides duplicated lines highlighter.

Config summary (see README.md for details):

    # file settings
    {
      "highlight_duplicates_color": "invalid"
    }

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

#Set whether the plugin is on or off
settings = sublime.load_settings('highlight_duplicates.sublime-settings')
plugin_enabled = bool(settings.get('highlight_duplicates_enabled', DEFAULT_IS_ENABLED))


def count_lines(lines, view):
    '''Counts line occurrences of a view using a hash.
    The lines are stripped and tested before count.
    '''
    counts = defaultdict(list)
    for line in lines:
        string = view.substr(line).strip()
        if is_candidate(string):
            counts[string].append(line)
    return counts


def filter_counts(counts, treshold=1):
    '''Filters the line counts by rejecting every line having a count
    lower or equal to the treshold, which defaults to 1.
    '''
    filtered = dict()
    for k, v in counts.iteritems():
        if len(v) > treshold:
            filtered[k] = v
    return filtered


def is_candidate(string):
    '''Tells if a string is a LOC candidate.
    A candidate is a string long enough after stripping some symbols.
    '''
    return len(string.strip('{}()[]/')) > 3


def show_lines(regions, view):
    '''Merges all duplicated regions in one set and highlights them.'''
    all_regions = []
    for r in regions:
        all_regions.extend(r)
    color_scope_name = settings.get('highlight_duplicates_color',
                                        DEFAULT_COLOR_SCOPE_NAME)
    view.add_regions('DuplicatesHighlightListener',
                        all_regions, color_scope_name,
                        sublime.DRAW_OUTLINED)


def highlight_duplicates(view):
    '''Main function that glues everything for hightlighting.'''
    # get all lines
    lines = view.lines(sublime.Region(0, view.size()))
    # count and filter out non duplicated lines
    duplicates = filter_counts(count_lines(lines, view))
    # show duplicated lines
    show_lines(duplicates.values(), view)


def downlight_duplicates(window):
    '''Removes any region highlighted by this plugin accross all views.'''
    for view in window.views():
        view.erase_regions('DuplicatesHighlightListener')


class HighlightDuplicatesCommand(sublime_plugin.WindowCommand):
    '''Actual Sublime command. Run it in the console with:
    view.window().run_command('highlight_duplicates')
    '''
    def run(self):
        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if plugin_enabled:
            highlight_duplicates(self.window.active_view())
        else:
            downlight_duplicates(self.window)


class DuplicatesHighlightListener(sublime_plugin.EventListener):
    '''Handles sone events to automatically run the command.'''
    def on_modified(self, view):
        if plugin_enabled:
            highlight_duplicates(view)

    def on_activated(self, view):
        if plugin_enabled:
            highlight_duplicates(view)

    def on_load(self, view):
        if plugin_enabled:
            highlight_duplicates(view)


class ToggleHighlightDuplicatesCommand(sublime_plugin.WindowCommand):
    def run(self):
        global plugin_enabled
        plugin_enabled = False if plugin_enabled else True

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if plugin_enabled:
            highlight_duplicates(self.window.active_view())
        else:
            downlight_duplicates(self.window)
