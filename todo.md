# TODO

## Bugs / Fixes
- [ ] Selecting all types for an app should exclude `inode/directory`
- [ ] Ctrl-C from console does not immediately terminate the app
- [x] Automatic defaults should be shown in SetDefaultAppDialog

## Features
- [x] UI: Get list of MIME types and associated applications
    - [x] Get some sort of item model going again
    - [x] Load all MIME types from QMimeDatabase
    - [x] Load associated application for each type
    - [x] Allow searching by MIME type or applications
- [x] UI: Set defaults by application
    - [x] Get list of mime types supported by an application
    - [x] Add app to Default Applications section
    - [x] Options to check / uncheck all supported types
    - [x] Toggle association / remove custom associations from this dialog
    - [ ] Add new custom associations from this window
    - [ ] Show selected/total defaults in the apps view
        - [ ] Add an option to only show apps with at least one MIME type association by default?
- [x] Add new file type to application
- [x] Remove file type from application
    - [x] Support removing entries from Added Associations
    - [x] Supporting adding things to Removed Associations
- [ ] Add ability to assign defaults to MIME types without any registered application yet (currently these file types are hidden entirely)
- [ ] Double clicking an option in SetDefaultAppDialog should toggle it as default
