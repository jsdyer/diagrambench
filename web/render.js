'use strict';
let loadError='';
function reportReady(){if(globalThis.mermaid?.render){parent.postMessage({type:'renderer-ready'},'*');return true;}if(loadError)parent.postMessage({type:'renderer-error',error:loadError},'*');return false;}
addEventListener('error',event=>{loadError=event.target?.id==='mermaid-library'?'The local Mermaid library could not load. Reload the page.':String(event.message||'The local renderer could not start.');parent.postMessage({type:'renderer-error',error:loadError},'*');},true);
addEventListener('DOMContentLoaded',reportReady);
addEventListener('load',reportReady);
addEventListener('message',event=>{if(event.source===parent&&event.data?.type==='renderer-status')reportReady();});
addEventListener('message', async event=>{if(event.source!==parent||!event.data||event.data.type!=='render')return;const {id,code,theme}=event.data;if(typeof code!=='string'||code.length>15000||typeof id!=='number')return;try{mermaid.initialize({startOnLoad:false,securityLevel:'strict',theme:['default','neutral','dark','forest'].includes(theme)?theme:'default',htmlLabels:false,flowchart:{htmlLabels:false},fontFamily:'Arial, sans-serif',maxTextSize:15000,maxEdges:250,suppressErrorRendering:true,secure:['securityLevel','startOnLoad','maxTextSize','maxEdges','htmlLabels','secure']});const result=await mermaid.render(`diagram${id}`,code,document.getElementById('scratch'));parent.postMessage({type:'rendered',id,svg:result.svg},'*');}catch(error){parent.postMessage({type:'rendered',id,error:String(error.message||error).slice(0,1500)},'*');}finally{document.getElementById('scratch').replaceChildren();}});
reportReady();
