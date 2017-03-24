# Rewriting Suplemon

## Rationale
The Suplemon project began as a POC. It proved to be a feasible idea and
worked well. However as the project progressed it became harder to add new
features since the core was too limiting. Supporting Python 2 and 3 at the same
time added unnecessary complexity. To fix this I'm rewriting the app from
scratch to be more flexible to work with. This will make it easier to implement
better and more advanced features.

## Major Architectural Changes
- Base all UI components on a shared base class with a good interface (widget)
- Allow arbitrary ordering of UI layout/widgets


## Features that should be added (or at least made possible)
- Render tab character as n spaces
- Support selecting text (regions)
- Per file settings (e.g. different tab width for different file types, support editorconfig)
- Split screen view (multiple files visible at the same time)
- Sidebar with directory tree (or anything else that's useful in a sidebar)
- Add a dropdown for autocomplete matches
- Proper plugin architecture (there's a lot that plugins can't do at the moment). Ultimately sublime plugins should be supported.
- Proper event system


## Whishlist
- Wrapping long lines
- Code folding
- Multi line prompts
- A menu for different commands at the top the screen (with mouse support)


## Tech
- General
> Use assert in (API) methods to make sure args are correct
> Use new-style classes: `class Buffer(object):`
> Setters return true or false depending on wether value changed


## Architecture

This is still pretty abstract and incomplete.

     __________________________
    |                          |
    |  COMMAND LINE INTERFACE  |
    |       Invokes App        |
    |__________________________|
        |
        |
    [Initialization parameters: files, debug, etc. Defaults used otherwise.]
        |
      \ | /
     __\|/_____________________
    |                          |
    | APP                      |
    |                          |
    |__________________________|
            
            
            
            
     __\|/_____________________
    |                          |
    | LAYOUT                   |
    |                          |
    |__________________________|



     _____________________________________________________________
    |                                                             |
    |                        EVENT LOOP                           |
    |                                                             |
    |_____________________________________________________________|
                 |                                   |             
                 |                                   |             
                 |                                   |             
                 |                                   |             
                 |                                   |             
                 |                                   |             
                 |                                   |             
         [Defered Rendering]                         |             
                 |                                   |             
     ____________|___________________                |             
    |                                |               |             
    |            RENDERER            |               |             
    |    (Render Layout to Screen)   |               |             
    |________________________________|               |             
                 |                                   |             
     ____________|___________________                |             
    |                                |               |             
    |            SCREEN              |               |             
    |     (Character Cell Grid)      |        [Buffered Input]     
    |________________________________|               |             
                 |                                   |             
     ____________|___________________________________|____________ 
    |            |                                   |            |
    |            |     INPUT / OUTPUT (BACKEND)      |            |
    |            |                                   |            |
    |          \ | /                                 |            |
    |     ______\|/___________          _____________|_______     |
    |    |                    |        |                     |    |
    |    |   Generic Output   |        |    Generic Input    | ---¦--- Abstracted to `InputEvent`s
    |    |____________________|        |_____________________|    |
    |             |                                  |            |
    |           \ | /                               /|\           |
    |            \|/                               / | \          |
    |             |_______________ __________________|            |
    |     ________|____      _____|________      ____|_______     |
    |    |             |    |              |    |            |    |
    |    |   Curses    |    |    Urwid?    |    |    PTPY?   |    |
    |    |_____________|    |______________|    |____________|    |
    |    _____________________________________________________    |
    |                            /|\                              |
    |                             |                               |
    |                             |                               |
    |     _______________________\|/_________________________     |
    |    [                                                   ]    |
    |    [                     TERMINAL                      ]    |
    |    [___________________________________________________]    |
    |                                                             |
    |_____________________________________________________________|



## Useful Unicode Symbols

    ⏎    23CE carriage return symbol
    ⌫    232B erase to the left (backspace)
    ␣    2423 space symbol

    ✓    2713 check mark
    ✗    2717 cross mark
    ×    00D7 multiplication sign
    ☠    2620 skull and crossbones

    ♻    267B black universal recycling symbol
