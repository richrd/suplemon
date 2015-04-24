# Developement plans (aiming for v.1.0.0)

This file is intended for planning and brainstorming
existing and new features for suplemon.

## Main Class Views
 * Needs support for more than editor views
     * A view is
         * Editor / Extension / Other /
           An entity that represents the view state and possible actions
         * Shows a "widget" in the app ui display area
         * Has acces to both status bars
         * Specifies key bindings and legend (or uses defaults)
         * Captures input if desired
         * The editor (file view) could be refactored into its own view
    * Migrate complex editor operations into extensions
        * [X] Commenting already exported
        * [ ] Type method might be a candidate
        * [ ] ...
    * Facilitate extensions running each other
        * And maybe "macros" by enabling combining commands
