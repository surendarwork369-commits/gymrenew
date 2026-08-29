import logging
import uuid

logger = logging.getLogger(__name__)


class MockWhatsAppService:
    """A simple mock provider so the reminder system can be built without a real API."""

    @staticmethod
    def send(phone, message):
        provider_message_id = f"mock-wa-{uuid.uuid4().hex[:12]}"
        logger.info("Sending mock WhatsApp message to %s", phone)
        return {
            "success": True,
            "provider_message_id": provider_message_id,
            "status": "queued",
            "message": message,
        }


def send_whatsapp_message(phone, message):
    """Public service function used by the reminder app."""
    if not phone:
        return {
            "success": False,
            "error": "No phone number available for this member.",
        }

    return MockWhatsAppService.send(phone, message)
