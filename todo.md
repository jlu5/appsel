# TODO

## Features to implement
- [x] UI: Get list of MIME types and associated applications
    - [x] Get some sort of item model going again
    - [x] Load all MIME types from QMimeDatabase
    - [x] Load associated application for each type
    - [ ] Allow searching by MIME type or applications
    - [ ] Add an option to only show MIME types that have at least one app associated?
- [x] UI: Set defaults by application
    - [x] Get list of mime types supported by an application
    - [x] Add app to Default Applications section
    - [x] Options to check / uncheck all supported types
    - [ ] Toggle association / remove custom associations from this dialog
    - [ ] Add new custom associations from this window
    - [ ] Add an option to only show apps with at least one MIME type association by default?
- [x] Add new file type to application
- [x] Remove file type from application
    - [x] Support removing entries from Added Associations
    - [x] Supporting adding things to Removed Associations
