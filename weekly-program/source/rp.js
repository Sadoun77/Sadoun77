const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+__dirname+'/prog.html');await p.evaluate(()=>document.fonts.ready);
await p.pdf({path:'prog.pdf',printBackground:true,preferCSSPageSize:true});await b.close()})();
