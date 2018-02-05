# -*- encoding: utf-8
"""
StatusBar components and renderer.
"""

import curses
import logging
from functools import partial
from wcwidth import wcswidth, wcwidth


class StatusComponent(object):
    """
    Base class for statusbar components
    Public API:
        .text              => unicode encoded content
        .style             => valid ncurses style or None
        .cells             => occupied terminal cell width
        .codepoints        => length of unicode codepoints
        .priority          => higher priority == less likey to be truncated, default 1
        .compute()         => maybe recalculate attributes and return serial
        .c_align(args)     => return truncated or padded copy of .text
        .attach_data(args) => attach transient data to component
        .get_data(args)    => get previously attached transient data
    """
    def __init__(self, text, style=None, priority=1):
        self._serial = 0
        self._data = None
        # Causes setters to be called
        # and self._serial being incremented
        self.text = text
        self.style = style
        self.priority = priority

    @property
    def cells(self):
        return self._cells

    @property
    def codepoints(self):
        return self._codepoints

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style
        self._serial += 1

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text
        self._cells = wcswidth(text)
        self._codepoints = len(text)
        self._serial += 1

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority
        self._serial += 1

    def compute(self):
        """
        Maybe recompute .text and/or .style and return new serial.
        This function serves two goals:
            - Allows a module to change it's output (clock, battery, file list, ..)
            - The return value may be used for higher level caching by the caller, e.g.
              a statusbar can refuse to update at all if none of its components report a
              change from the previous call and it's size did not change either.

        For simple StatusBarComponents the default implementation should suffice:
        Every time component.text or component.style is changed an internal _serial var is
        incremented and will be returned here.

        More complex components can implement this on their own.

        The return value is not a simple boolean because a component may be used in
        multiple places at once, each having its own idea of the current state.
        Thus having this function change some internal boolean would deliver the wrong
        result for all callers after the first one.
        """

        # 1. Implement own logic to detect if recomputing .text or .style is necessary
        # 2. If yes: update .text and/or .style
        # 3. return current serial
        return self._serial

    def attach_data(self, identifier, data):
        """allow external callers to attach data to this component"""
        if self._data is None:
            self._data = dict()
        self._data[identifier] = data

    def get_data(self, identifier, alt=None):
        """allow external callers to read attached data from this component"""
        _data = self._data
        return alt if _data is None else _data.get(identifier, alt)

    def c_align(self, width, start_right=True, fillchar=" "):
        """
        Pad or truncate text based on actual used characters instead of unicode codepoints.
        Returns a tuple of (state, text).
        state is a single integer holding the amount of characters added (positive), deleted (negative)
        or 0 if there was nothing to do.
        """

        delta = width - self._cells
        if delta == 0:
            # nothing to do. fix 'yo coll'ar
            return (0, self._text)

        _text = self._text
        if delta > 0:
            # pad, start_right means text starts right means pad left
            if start_right:
                return (delta, fillchar * delta + _text)
            else:
                return (_text + fillchar * delta)

        delta_p = delta * -1
        if self._cells == self._codepoints:
            # truncate - codepoints
            if start_right:
                return (delta, _text[:delta])
            else:
                return (delta, _text[delta_p:])

        cells = 0
        if start_right:
            # truncate - chars - right
            codepoints = 0
            while cells < delta_p:
                codepoints -= 1
                cells += wcwidth(_text[codepoints])
            _text = _text[:codepoints]
            if cells > delta_p:
                # Deleted too much, multi cell codepoint at end of deletion
                _text += fillchar * (cells - delta_p)
            return (delta, _text)

        # truncate - chars - left
        codepoints = 0
        while cells < delta_p:
            cells += wcwidth(_text[codepoints])
            codepoints += 1
        _text = _text[codepoints:]
        if cells > delta_p:
            # Deleted too much, multi cell codepoint at end of deletion
            _text = fillchar * (cells - delta_p) + _text
        return (delta, _text)


class StatusComponentShim(StatusComponent):
    """
    Wraps some function call into a StatusBarComponent.
    This allows the caller to use caching information but will
    call the provided function all the time which may be expensive.
    Mainly used for compability of old modules without the new interface.
    """
    def __init__(self, function):
        StatusComponent.__init__(self, "n/a")
        self._producer = function

    def compute(self):
        text = self._producer()
        if self.text != text:
            self.text = text
        return self._serial


class StatusComponentFill(object):
    style = None


class StatusComponentGenerator(object):
    """
    Generates StatusComponents on demand, useful for e.g. filelist.
    Provides compute() to detect changes and regenerate or modify
    components but does neither provide .text nor .style.
    StatusBar will call compute() and if necessary get_components().
    """
    def __init__(self):
        self._serial = 0
        self._data = None
        self._components = list()

    def compute(self):
        # Maybe regenerate or modify self._components
        # and increment self._serial
        return self._serial

    def get_components(self):
        return self._components

    def get_data(self, identifier, alt=None):
        _data = self._data
        return alt if _data is None else _data.get(identifier, alt)

    def attach_data(self, identifier, data):
        if self._data is None:
            self._data = {}
        self._data[identifier] = data


class StatusBarManager(object):
    def __init__(self, app):
        self._app = app
        self._bars = []
        self.logger = logging.getLogger("%s.%s" % (__name__, self.__class__.__name__))
        self._init_components()

    def _init_components(self):
        self.components = {}
        modules = self._app.modules.modules
        for module_name in sorted(modules.keys()):
            module = modules[module_name]
            if callable(getattr(module, "get_components", None)):
                # New interface
                for name, comp in module.get_components():
                    self.components[name.lower()] = comp(self._app)
                    self.logger.info("Module '%s' provides component '%s'." % (module_name, name))
            elif module.options["status"]:
                # Old interface, use shim
                comp = StatusComponentShim(module.get_status)
                self.components[module_name.lower()] = comp
                self.logger.info("Module '%s' provides old status interface. Using shim." % module_name)
        self.components["fill"] = StatusComponentFill

    def add(self, win, config_name):
        bar = StatusBar(self._app, win, self, config_name)
        self._bars.append(bar)
        return bar

    def render(self):
        for bar in self._bars:
            bar.render()

    def force_redraw(self):
        """Forces a redraw of all statusbars on the next run"""
        # For some reason automatic detection of size changes triggers
        # earlier for startsbars than for the rest of the application.
        # This means statusbars will detect a size change, state will
        # get invalidated, new content will be calculated and drawn.
        # Then the resize logic of the application itself will kick in,
        # do an erase() on screen and layout everything. Meanwhile all
        # statusbars are already aware of the new size and will refuse
        # to redraw unless some component inside a given bar reports
        # a change and thus invalidates the state of the bar.
        # bar.force_redraw() simply resets the internal cached size
        # of the bar which will then trigger a redraw on the next run.
        #
        # FIXME: rename to reset or invalidate_state or something as
        #        this thing doesn't redraw anything.
        for bar in self._bars:
            bar.force_redraw()


class StatusBar(object):
    def __init__(self, app, win, manager, config_name):
        self.app = app
        self._win = win
        self._manager = manager
        self._component_string = None
        self._components = []
        self._size = None
        self._config_name = config_name
        self.logger = logging.getLogger("%s.%s.%s" % (__name__, self.__class__.__name__, config_name))
        self.update_config()
        self.app.set_event_binding("config_loaded", "after", self.update_config)
        # FIXME: figure out why config reload trigger does not reset size

    def update_config(self, e=None):
        self.logger.debug("Config update detected")
        config = self.app.config["display"].get(self._config_name, None)
        if not config:
            self.logger.warning("No display config for statusbar '%s' found" % self._config_name)
            return
        self.FILL_CHAR = config["fillchar"]
        self.SPACE_CHAR = config["spacechar"]
        self._truncate_direction = config["truncate"]
        self._default_align = config["default_align"]
        if self._truncate_direction == "right":
            self._truncate_right = True
        else:
            self._truncate_right = False
        if self._component_string != config["components"]:
            self._component_string = config["components"]
            self.logger.info("Components changed to '%s'" % self._component_string)
            self._load_components()
        # FIXME: force_redraw is called twice, here and in ui.py on resize() handler
        #        which in turn is called by main.py after emitting config_loaded event
        self.force_redraw()
        # FIXME: figure out why this is not enough
        # self.render()

    def _load_components(self):
        # Python2 has no list.clear()
        # self._components.clear()
        del self._components[:]
        for name in self._component_string.split(" "):
            name_l = name.lower()
            comp = self._manager.components.get(name_l, None)
            if comp is None:
                self.logger.warning("No StatusBar component with name '%s' found." % name_l)
                comp = StatusComponent(name)
                self._components.append(comp)
                continue
            self._components.append(comp)

    def force_redraw(self):
        """Force redraw on next run"""
        # FIXME: rename to reset or invalidate_state or something as
        #        this thing doesn't redraw anything.
        self._size = None

    @property
    def size(self):
        return self._size

    def compute_size(self):
        size = self._win.getmaxyx()[1]
        if size != self._size:
            self.logger.debug("%s size changed from %s to %i" % (self._win, self._size, size))
            self._size = size
            return True
        return False

    def _calc_spacing_required(self, components):
        # Include spacing between components if none of:
        #   next element is fill
        #   next element.cells == 0
        #   last element
        cells = 0
        max_index = len(components) - 1
        for index, comp in enumerate(components):
            if comp is StatusComponentFill:
                continue
            cells += comp.cells
            if index == max_index:
                continue
            nextComp = components[index + 1]
            if nextComp is not StatusComponentFill and nextComp.cells > 0:
                cells += 1
        return self.size - cells

    def _truncate(self, components):
        # 1. Removes all fills (which will then automatically be replaced by spacers)
        #    => ensures there is always a spacer between components
        # 2. Recalculates size
        #    => usually no spacers will be drawn if the next component is a fill
        # 3. Removes components and/or truncates last/first component (depending on direction)
        # 4. Returns a tuple of (new_spacing_required, [(truncate, c) for c in components])

        # Remove fills
        components = [c for c in components if c is not StatusComponentFill]
        overflow = self._calc_spacing_required(components) * - 1

        # Move forward or backwards / truncate left or right
        _results = []
        _truncate_right = self._truncate_right
        if _truncate_right:
            _iter = range(len(components) - 1, - 1, - 1)
            _add = partial(_results.insert, 0)
        else:
            _iter = range(len(components))
            _add = _results.append

        FILL_CHAR = self.FILL_CHAR
        for index in _iter:
            component = components[index]
            if overflow <= 0:
                # Enough truncated / add to _results
                _add((None, component))
                continue
            usage = component.cells
            if overflow > usage:
                # Remove component / don't add to _results
                overflow -= usage
                overflow -= 1      # remove spacing
            else:
                # Dry run component truncate and add
                # instruction how much to truncate to _results
                truncated, _ = component.c_align(
                    usage - overflow,
                    start_right=_truncate_right,
                    fillchar=FILL_CHAR
                )
                _add((usage - overflow, component))
                overflow += truncated                # c_align is negative on truncate

        return (overflow * - 1, _results)

    def _get_fill(self, fill_count, spacing_required):
        """
        Try to distribute required spacing evenly between fill components
        Returns fill, fill_missing
        """
        if fill_count == 0 or spacing_required == 0:
            return (None, None)

        FILL_CHAR = self.FILL_CHAR
        if fill_count == 1:
            fill_size = spacing_required
            fill_missing = None
        else:
            fill_size = spacing_required // fill_count
            fill_missing = FILL_CHAR * (spacing_required - fill_size * fill_count)
        return (FILL_CHAR * fill_size, fill_missing)

    def _align(self, components):
        """Add fills to match alignment of left, center or right"""
        align = self._default_align
        if align == "left":
            components.append(StatusComponentFill)
            fill_count = 1
        elif align == "right":
            components.insert(0, StatusComponentFill)
            fill_count = 1
        elif align in {"center", "middle", "centre"}:
            components.insert(0, StatusComponentFill)
            components.append(StatusComponentFill)
            fill_count = 2
        else:
            self.logger.warning(
                "align is not any of left, right, center, middle, centre." +
                "Using left alignment. Given value was '%s'. Please fix your config." % align
            )
            components.append(StatusComponentFill)
            fill_count = 1
        return fill_count

    def _changes_pending(self):
        """Ask all components to maybe recompute + figure out if something changed"""
        changed = False
        _state = "sb_{}_state".format(id(self))
        for comp in self._components:
            if comp is StatusComponentFill:
                continue
            serial = comp.compute()
            if serial != comp.get_data(_state):
                # No break here: all modules have a chance to compute()
                changed = True
                comp.attach_data(_state, serial)
        # Always call compute_size() to detect screen width change
        return self.compute_size() or changed

    def render(self):
        """Render status line based on components in parts list"""

        if not self._changes_pending():
            # self.logger.debug("no changes")
            return

        # self.logger.debug("something changed, doing all the buzz")

        # Create a new component list and, if required, expand it
        _components = []
        for comp in self._components:
            if isinstance(comp, StatusComponentGenerator):
                _components.extend(comp.get_components())
            else:
                _components.append(comp)

        spacing_required = self._calc_spacing_required(_components)
        fill_count = sum(1 for x in _components if x is StatusComponentFill)

        # Default alignment
        if spacing_required and fill_count == 0:
            fill_count = self._align(_components)

        # Truncate
        if spacing_required > fill_count:
            _components = [(None, comp) for comp in _components]
        else:
            # TODO: spacing_required should be omitted: we removed all fills
            #       or: add a fill in _truncate() if spacing_required > 0
            #       and return fill_count instead of spacing_required
            spacing_required, _components = self._truncate(_components)
            fill_count = 0

        # Try to distribute required spacing evenly between fill components
        fill, fill_missing = self._get_fill(fill_count, spacing_required)

        # Render components
        FILL_CHAR = self.FILL_CHAR
        SPACE_CHAR = self.SPACE_CHAR
        _truncate_right = self._truncate_right
        _win = self._win
        _win.move(0, 0)
        last_index = len(_components) - 1
        for index, item in enumerate(_components):
            trunc_newlen, component = item
            if component is not StatusComponentFill:
                if trunc_newlen is None:
                    data = component.text
                else:
                    _, data = component.c_align(
                        trunc_newlen,
                        start_right=_truncate_right,
                        fillchar=FILL_CHAR
                    )
            elif fill_missing:
                # Required spacing was not evenly distributed.
                # Compensate by making first fill larger by difference
                data = fill + fill_missing
                fill_missing = None
            else:
                data = fill
            if data:
                try:
                    if component.style is not None:
                        # self.logger.debug(
                        #    "Rendering data with style starting at col %i: '%s'" % (_win.getyx()[1], data)
                        # )
                        _win.addstr(data, component.style)
                    else:
                        # self.logger.debug(
                        #    "Rendering data without style starting at col %i: '%s'" % (_win.getyx()[1], data)
                        # )
                        _win.addstr(data)
                except curses.error as e:
                    # self.logger.debug("curses error")
                    if index != last_index:
                        # Only care if we are not writing the last component.
                        # The reason is ncurses will always return an error on
                        # writes to the last cell of a non scrolling region.
                        # See man pages for:
                        #   addstr (inherit errors from waddch)
                        #   waddch (scrollok not enabled: write succeeds but cursor position can't be advanced)
                        # Wishlist: Ncurses could really use some different or additional error codes to indicate this.
                        #
                        # This will also trigger if none of the following components
                        # write anything like .cells == 0 or empty fills.
                        self.logger.debug(
                            "Got a curses error for index %i/%i with content '%s': %s" %
                            (index, last_index, data, e)
                        )
            if index == last_index:
                continue
            nextComp = _components[index + 1][1]
            if StatusComponentFill not in (component, nextComp) and nextComp.cells > 0:
                # Draw spacer independently of component to use the statusbar style.
                try: _win.addstr(SPACE_CHAR)   # noqa E701
                except: pass                   # noqa E701
        # Mark window as new content but do not update the screen yet
        _win.noutrefresh()
