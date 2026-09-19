const API="/api";
function user(){return JSON.parse(localStorage.getItem("alumniUser")||"null")}
function requireLogin(){const u=user();if(!u)location.href="login.html";return u}
async function api(path,opt={}){const r=await fetch(API+path,{headers:{"Content-Type":"application/json"},...opt});const d=await r.json().catch(()=>({}));if(!r.ok)throw Error(d.error||"Request failed");return d}
document.addEventListener("DOMContentLoaded",()=>{const l=document.getElementById("logout");if(l)l.onclick=e=>{e.preventDefault();localStorage.removeItem("alumniUser");location.href="login.html"}})
