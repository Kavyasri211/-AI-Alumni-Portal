requireLogin();
(async()=>{let d=await api("/events");eventsList.innerHTML=d.events.map(e=>`<div class="event"><b>${e.event_date} · ${e.location}</b><h3>${e.title}</h3><p>${e.description}</p></div>`).join("")})();
generateInvite.onclick=async()=>{aiResult.textContent="Generating...";let d=await api("/ai/generate",{method:"POST",body:JSON.stringify({kind:"event_invitation",event_title:eventTitle.value||"Alumni Networking Event",details:eventDetails.value})});aiResult.textContent=d.result}
