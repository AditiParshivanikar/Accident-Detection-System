import time
import logging
from sqlalchemy.orm import Session
from .models import Settings

logger = logging.getLogger(__name__)

# Try importing twilio
TWILIO_AVAILABLE = False
try:
    from twilio.rest import Client
    TWILIO_AVAILABLE = True
except ImportError:
    logger.warning("twilio package not installed. SMS alerts will be unavailable until installed.")

# Global rate limiting variable
last_sms_sent_time = 0.0
COOLDOWN_SECONDS = 60.0

def send_accident_alert(db: Session, confidence: float = 0.0, vehicle_count: int = 0):
    """
    Sends an SMS alert using Twilio if configured and cooldown has passed.
    """
    global last_sms_sent_time

    # Fetch settings
    settings = db.query(Settings).first()
    if not settings:
        logger.warning("No settings found in database. Cannot check Twilio alert status.")
        return False

    if not settings.twilio_enabled:
        return False

    # Check cooldown
    current_time = time.time()
    if current_time - last_sms_sent_time < COOLDOWN_SECONDS:
        logger.info(f"SMS Alert skipped: inside cooldown period. Time remaining: {int(COOLDOWN_SECONDS - (current_time - last_sms_sent_time))}s")
        return False

    if not TWILIO_AVAILABLE:
        logger.error("Twilio package is missing. Cannot send SMS. Install twilio via pip.")
        return False

    # Check for empty credentials
    if not settings.twilio_sid or not settings.twilio_token or not settings.twilio_from or not settings.twilio_to:
        logger.error("Twilio credentials are incomplete. Please update them in settings.")
        return False

    try:
        logger.info("Initializing Twilio client...")
        client = Client(settings.twilio_sid, settings.twilio_token)
        
        message_body = (
            f"🚨 ACCIDENT DETECTED! 🚨\n"
            f"An accident collision has been detected by the AI Alert System.\n"
            f"Details:\n"
            f"- Date/Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n"
            f"- Vehicles Involved: {vehicle_count}\n"
            f"- Confidence Score: {confidence:.2f}\n"
            f"Please check the live system dashboard immediately."
        )

        logger.info(f"Sending SMS via Twilio from {settings.twilio_from} to {settings.twilio_to}...")
        message = client.messages.create(
            body=message_body,
            from_=settings.twilio_from,
            to=settings.twilio_to
        )
        
        # Update cooldown
        last_sms_sent_time = current_time
        logger.info(f"SMS Alert sent successfully. Message SID: {message.sid}")
        return True

    except Exception as e:
        logger.error(f"Failed to send SMS via Twilio: {e}")
        return False

def trigger_test_sms(db: Session) -> dict:
    """
    Triggers a test SMS bypasses cooldown to verify connection settings.
    """
    settings = db.query(Settings).first()
    if not settings:
        return {"success": False, "message": "No settings found in database."}

    if not TWILIO_AVAILABLE:
        return {"success": False, "message": "Twilio library is not installed."}

    if not settings.twilio_sid or not settings.twilio_token or not settings.twilio_from or not settings.twilio_to:
        return {"success": False, "message": "Twilio parameters are incomplete."}

    try:
        client = Client(settings.twilio_sid, settings.twilio_token)
        message_body = "🚨 TEST ALERT: Twilio SMS configuration for Accident Detection System verified successfully!"
        
        message = client.messages.create(
            body=message_body,
            from_=settings.twilio_from,
            to=settings.twilio_to
        )
        return {"success": True, "message": f"Test SMS sent successfully. SID: {message.sid}"}
    except Exception as e:
        return {"success": False, "message": f"Twilio Error: {str(e)}"}
