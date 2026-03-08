# Research Notes

## City of Saskatoon Rec Site
**URL:** https://apps5.saskatoon.ca/app/qRecTracDropin/DropinPrograms

### How it works
- Old-school ASP.NET form — no API, just a POST request
- Page reloads with results after form submission
- BeautifulSoup will work perfectly, no Playwright needed

### HTML Structure
- Results in a table: `id="tpwebsearch_output_table"`
- Each event row: `<td class="label-cell" data-title="Description">`
- Begin Time: `<td class="label-cell" data-title="Begin Time">`
- End Time: `<td class="label-cell" data-title="End Time">`

### POST Form Fields
- `ctl00$MainContent$lstKeywordSearch` = `All` (or specific activity)
- `ctl00$MainContent$Facility` = `All` (or specific facility)
- `ctl00$MainContent$ProgramTypes` = `All`
- `ctl00$MainContent$SearchBy` = `radiobtnDaily`
- `ctl00$MainContent$BtnSearchPrograms` = `Search`
- `__VIEWSTATE` = (long token — must be fetched fresh each time)

### Strategy for Session 12
1. GET the page first to grab the __VIEWSTATE token
2. POST with form data + token + desired date
3. Parse the results table with BeautifulSoup

### Location field
- Location is embedded in the Program Description (e.g. "Shaw - Hot Tub")
- Format is usually "FacilityName - ProgramName"
