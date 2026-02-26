1.0.5

*Minor Features*
- Added ability to add notes to scenarios
- Update limits of groundwater components
- Changed spray areation model to use user defined efficiency instead of estimated efficiency
- Added ability to change models in the design view

1.0.4

*Major Features*
Amanzi is now capable of running scenarios in the browser using Pyodide, no longer requiring a Python server.


1.0.3

*Bug Fixes*
- Fixed duplicate connections not being removed from the scenario in rare cases
- Changed font size of the quick results to be smaller

1.0.2

*Minor Features*
- Added reset to default button
- Added sustainability metrics to the dosing model
- Set default locale to browser language
- Modified vacuum design to display per m3, per unit and total process
- Added dry and wet gas composition to vacuum design

*Bug Fixes*
- Fixed oxygen balance not correct when using redox uncoupled oxygen in conjunction with normal oxygen
- Fixed report window not opening to selected scenario
- Fixed quality chart paths not recalcuting when selecting a different scenario in report view
- Fixed display error with bar values close to zero
- Fixed h2s being calculated incorrectly in vacuum design due to it being calculated as Seaborgium (Sg) instead of Hydrogen Sulfide (H2S)