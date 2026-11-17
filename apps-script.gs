/**
 * Backend for the guest wishes/RSVP (optional).
 * 1. Create a Google Sheet, then open Extensions > Apps Script and paste this file.
 * 2. Deploy > New deployment > Web app: Execute as "Me", Who has access "Anyone".
 * 3. Copy the Web App URL into CONFIG.rsvpEndpoint in index.html.
 */
const SHEET = 'Ucapan';

function sheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  return ss.getSheetByName(SHEET) || ss.insertSheet(SHEET).appendRow(['ts', 'name', 'att', 'msg']).getSheet();
}

function doGet() {
  const rows = sheet_().getDataRange().getValues().slice(1);
  const data = rows.map(r => ({ ts: Number(r[0]), name: String(r[1]), att: String(r[2]), msg: String(r[3]) }));
  return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  const clean = (s, n) => String(s || '').replace(/^[=+\-@]/, "'$&").slice(0, n);
  if (!d.name || !d.msg || !['y', 'n'].includes(d.att)) return ContentService.createTextOutput('invalid');
  sheet_().appendRow([Date.now(), clean(d.name, 60), d.att, clean(d.msg, 500)]);
  return ContentService.createTextOutput('ok');
}
