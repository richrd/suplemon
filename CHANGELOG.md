Change Log
==========

## [v0.1.56](https://github.com/richrd/suplemon/tree/v0.1.56) (2016-08-01) compared to previous master branch.
[Full Changelog](https://github.com/richrd/suplemon/compare/v0.1.55...v0.1.56)

**Implemented enhancements:**

- New feature: Ability to use hard tabs instead of spaces via the boolean option 'hard_tabs'.
- New feature: Save all files by running the ´save_all´ command.
- New feature: Linter now shows PHP syntax errors (if PHP is installed).
- New module: New `diff` command for comaring current edits to the file on disk.
- New module: Show machine hostname in bottom status bar.
- Enhanced Go To feature: If no file name begins with the search string, also match file names that contain the search string at any position.
- Module status info is now shown on the left of core info in the bottom status bar.
- More supported key bindings.
- Other light code improvements.

**Fixed bugs:**

- Prevented multiple warnings about missing pygments.
- Reload user keymap when it's changed in the editor.
- Prioritize user key bindings over defaults. [\#163](https://github.com/richrd/suplemon/issues/163)
- Reworked key handling to support more bindings (like `ctrl+enter` on some terminals).
- Normalize modifier key order in keymaps so that they are matched correctly.
- Properly set the internal file path when saving a file under a new name.

## [v0.1.55](https://github.com/richrd/suplemon/tree/v0.1.55) (2016-08-01) compared to previous master branch.
[Full Changelog](https://github.com/richrd/suplemon/compare/v0.1.54...v0.1.55)

**Implemented enhancements:**

- Faster loading when linting lots of files

- Use `invisibles` setting in TextMate themes [\#77](https://github.com/richrd/suplemon/issues/77)

**Fixed bugs:**

- Show key legend based on config instead of static defaults [\#157](https://github.com/richrd/suplemon/issues/157)


## [v0.1.54](https://github.com/richrd/suplemon/tree/v0.1.54) (2016-07-30) compared to previous master branch.
[Full Changelog](https://github.com/richrd/suplemon/compare/v0.1.53...v0.1.54)

**Implemented enhancements:**

- Autocomplete in open/save dialogs

**Fixed bugs:**

- Fixed showing unwritable marker when saving file in a writable location


## [v0.1.32](https://github.com/richrd/suplemon/tree/v0.1.32) (2015-08-12) compared to previous master branch.
[Full Changelog](https://github.com/richrd/suplemon/compare/v0.1.31...v0.1.32)

**Implemented enhancements:**

- Use Sphinx notation for documenting parameters/return values etc [\#54](https://github.com/richrd/suplemon/issues/54)
- Pygments syntax highlighting [\#52](https://github.com/richrd/suplemon/issues/52)
- Make jumping between words also jump to next or previous line when applicable. [\#48](https://github.com/richrd/suplemon/issues/48)
- Retain cursor x coordinate when moving vertically. [\#24](https://github.com/richrd/suplemon/issues/24)
- Add line number coloring to linelighters. [\#23](https://github.com/richrd/suplemon/issues/23)
- Native clipboard support [\#73](https://github.com/richrd/suplemon/issues/73)
- Installing system-wide [\#75](https://github.com/richrd/suplemon/issues/75)
- Added a changelog. The new version is much more mature than before, and there are a lot of changes. That's why this is the first changelog (that should have existed long before)

**Closed issues:**

- Auto hide keyboard shortcuts from status bar  [\#70](https://github.com/richrd/suplemon/issues/70)

**Fixed bugs:**

- Using delete at the end of multiple lines behaves incorrectly [\#74](https://github.com/richrd/suplemon/issues/74)

**Merged pull requests:**

- Implemented jumping between lines. Fixes \#48. [\#72](https://github.com/richrd/suplemon/pull/72) ([richrd](https://github.com/richrd))
- Pygments-based highlighting [\#68](https://github.com/richrd/suplemon/pull/68) ([Jimx-](https://github.com/Jimx-))
