from django.http import HttpResponse, JsonResponse
from Events.models import Event, EventAlumni
from Alumni.models import alumni
from Notifications.models import Notification
from .services import TwilioClient
from django.views.decorators.csrf import csrf_exempt
from main import settings
from twilio.rest import Client

replycli = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)



cli = TwilioClient()
def test_fnc(request):
    cli.send_rsvp_confirmation(to='')
    return HttpResponse("Done")

def send_message_view(data: Notification):
    message = f"Hello Alumni! Don't miss our upcoming events.\n{data.n_content} about {data.event_id.event_name} on {data.event_id.event_date}"
    cli.send_general_message(message, data)
    return JsonResponse({'status': 'General message sent'})

def send_update_view(event_id:int):
    event = Event.objects.get(event_id=event_id)
    update_message = "This is a friendly reminder for the event."
    cli.send_rsvp_updates(event, update_message)
    return JsonResponse({'status': 'Update sent to RSVP\'d users'})

@csrf_exempt
def bot(request):
    
    message = request.POST["Body"]
    to = request.POST["From"]
    
    if message == "YES":
        eveid = int(request.POST["ButtonPayload"])
        replycli.messages.create(
            from_= f'whatsapp:+{settings.TWILIO_WHATSAPP_NUMBER}',
            body='Thank you for confirming your attendance!!',
            to=to,
        )
        eve = Event.objects.get(event_id = eveid)
        to = to[10:]
        to = int(to)
        al = alumni.objects.get(phone_number= to)
        EventAlumni.objects.create(event_id = eve, alumni_id = al)
    elif message == "NO":
        replycli.messages.create(
            from_= f'whatsapp:+{settings.TWILIO_WHATSAPP_NUMBER}',
            body='Sorry to hear that you can\'t make it!!',
            to=to,
            )
    return HttpResponse("Done")

