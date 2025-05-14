from django.shortcuts import render
from lms. queryProxy import QueryCacheProxy
from django.core.cache import cache
import json
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils.timezone import localtime, now
from django.contrib.auth.decorators import login_required

def parse_flexible_timestamp(raw_timestamp, output_format="%b %d, %Y %I:%M %p"):
    """
    Parses ISO8601 or human-readable timestamp strings.
    Returns a formatted string or "Invalid Time" if parsing fails.
    """
    if not raw_timestamp or not isinstance(raw_timestamp, str):
        return "Invalid Time"

    cleaned = raw_timestamp.strip().replace('\xa0', ' ')  # Clean up invisible chars

    parsed = parse_datetime(cleaned)  # Try ISO8601 first
    if not parsed:
        try:
            parsed = datetime.strptime(cleaned, "%b %d, %Y %I:%M %p")
        except ValueError:
            return "Invalid Time"

    # Localize the time
    localized = localtime(parsed)
    return localized.strftime(output_format)

@login_required
def get_cached_chat_messages(request,ins_id):
    group_key = f"chat_{ins_id}"
    index_key = f"{group_key}:index"
    message_keys = cache.get(index_key, [])
    messages = []
    valid_keys = []

    for key in message_keys:
        msg = cache.get(key)
        if msg:
            messages.append(json.loads(msg))  # Parse back to dict
            valid_keys.append(key)

    # Clean expired keys from index
    cache.set(index_key, valid_keys, timeout=3600)

    return messages

@login_required
def commChat(request, ins_id):
    proxy = QueryCacheProxy(request.user)
    institute = proxy._get_institute(ins_id)
    messages = get_cached_chat_messages(request,ins_id)
    print(messages)
    for msg in messages:
        # Ensure sender ID is int for safe comparison in template
        if isinstance(msg.get("sender"), dict) and "id" in msg["sender"]:
            msg["sender"]["id"] = int(msg["sender"]["id"])
        # Convert ISO timestamp string to localized datetime object
        msg["timestamp"] = parse_flexible_timestamp(msg.get("timestamp"))
        print(msg["timestamp"])


    context = {
        'institute': institute,
        'chatMessages': messages
    }
    return render(request, 'commChat.html', context)
