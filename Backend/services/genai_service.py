import os
def generate_content(x):
    kind=x.get("kind","networking_summary"); name=x.get("name","Alumni")
    details=x.get("details","professional networking and knowledge sharing")
    event=x.get("event_title","Alumni Networking Event")
    if os.getenv("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            client=OpenAI()
            prompts={
              "networking_summary":f"Write a concise professional alumni networking summary for {name}. Context: {details}",
              "event_invitation":f"Write a warm professional invitation for alumni to attend {event}. Details: {details}",
              "professional_message":f"Write a short professional networking message from {name}. Context: {details}",
              "engagement_insights":f"Give 4 concise alumni engagement insights based on: {details}"
            }
            r=client.responses.create(model=os.getenv("OPENAI_MODEL","gpt-4o-mini"),input=prompts.get(kind,prompts["networking_summary"]))
            return r.output_text
        except Exception:
            pass
    return {
      "networking_summary":f"Connect with alumni working in related fields who share your skills and interests. {details}. Shared experience can create meaningful professional opportunities.",
      "event_invitation":f"You're invited to {event}. Join fellow alumni to reconnect, exchange industry insights and discover new professional opportunities. {details}",
      "professional_message":f"Hi, I’m {name}. I’d be glad to connect and exchange professional insights. {details}",
      "engagement_insights":"1. Invite alumni with related skills to networking groups. 2. Use events to reconnect inactive members. 3. Encourage mentoring. 4. Share relevant career and industry updates."
    }.get(kind,"AI-generated alumni networking content.")
