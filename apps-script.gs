// Backend undangan Sifa & Yoga (Google Sheets): ucapan tamu + teks pesan WhatsApp.
// Tab "Ucapan": ucapan tamu (hapus baris untuk menghapus ucapan).
// Tab "Pesan WA": edit sel A2 untuk mengubah pesan WhatsApp. {nama} dan {link} diganti otomatis.
// Setelah mengubah kode ini: Deploy > Manage deployments > Edit > Version: New version > Deploy.
const SH='Ucapan',PS='Pesan WA';
const DEF=`Assalamu'alaikum Warahmatullahi Wabarakatuh

Kepada Yth.
Bapak/Ibu/Saudara/i *{nama}*

Tanpa mengurangi rasa hormat, perkenankan kami mengundang Bapak/Ibu/Saudara/i untuk menghadiri acara pernikahan kami:

*Sifa & Yoga*
Minggu, 27 Desember 2026
Sakha Ballroom, Royal Sentul Park

Info lengkap acara dan konfirmasi kehadiran:
{link}

Merupakan suatu kehormatan dan kebahagiaan bagi kami apabila Bapak/Ibu/Saudara/i berkenan hadir dan memberikan doa restu.

Wassalamu'alaikum Warahmatullahi Wabarakatuh

Kami yang berbahagia,
Sifa & Yoga`;
function sh_(){const s=SpreadsheetApp.getActiveSpreadsheet();let h=s.getSheetByName(SH);if(!h){h=s.insertSheet(SH);h.appendRow(['ts','name','att','msg']);}return h;}
function ps_(){const s=SpreadsheetApp.getActiveSpreadsheet();let p=s.getSheetByName(PS);if(!p){p=s.insertSheet(PS);p.getRange('A1').setValue('Edit pesan WhatsApp di sel A2. {nama} = nama tamu, {link} = link undangan. Teks di antara *bintang* tampil tebal.').setFontWeight('bold');p.getRange('A2').setValue(DEF).setWrap(true).setVerticalAlignment('top');p.setColumnWidth(1,700);p.setRowHeight(2,520);}return p;}
function out_(o){return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);}
function doGet(e){if(e&&e.parameter&&e.parameter.pesan){const t=String(ps_().getRange('A2').getValue()||'').trim();return out_({pesan:t||DEF});}
const h=sh_(),n=h.getLastRow();if(n<2)return out_([]);return out_(h.getRange(2,1,n-1,4).getValues().filter(r=>r[1]&&r[3]).map(r=>({ts:+r[0]||0,name:String(r[1]),att:r[2]=='n'?'n':'y',msg:String(r[3])})).sort((a,b)=>b.ts-a.ts));}
function doPost(e){let d;try{d=JSON.parse(e.postData.contents)}catch(x){return out_({ok:false})}
const c=(s,n)=>String(s||'').trim().slice(0,n).replace(/^[=+\-@]/,"'$&");const nm=c(d.name,60),ms=c(d.msg,500),at=d.att=='n'?'n':d.att=='y'?'y':'';
if(!nm||!ms||!at)return out_({ok:false});const l=LockService.getScriptLock();l.waitLock(10000);
try{const h=sh_(),n=h.getLastRow();if(n>=2){const f=Math.max(2,n-19),r=h.getRange(f,1,n-f+1,4).getValues();if(r.some(x=>String(x[1])==nm&&String(x[3])==ms&&Date.now()-x[0]<120000))return out_({ok:true});}
h.appendRow([Date.now(),nm,at,ms]);}finally{l.releaseLock()}return out_({ok:true});}
function setup(){ps_();sh_();}
