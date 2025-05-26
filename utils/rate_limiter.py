from datetime import datetime, timedelta
import threading
from collections import deque

class RateLimiter:
    def __init__(self, max_rpm, max_tpm, max_rpd):
        self.max_rpm = max_rpm
        self.max_tpm = max_tpm
        self.max_rpd = max_rpd
        
        self.requests_lock = threading.Lock()
        self.minute_requests = deque(maxlen=60)
        self.day_requests = deque(maxlen=24*60)
        self.tokens_per_minute = 0
        
    def can_make_request(self, estimated_tokens=0):
        with self.requests_lock:
            current_time = datetime.now()
            
            # Clean up old requests
            self._cleanup_old_requests(current_time)
            
            # Check rate limits
            if (len(self.minute_requests) >= self.max_rpm or
                self.tokens_per_minute + estimated_tokens > self.max_tpm or
                len(self.day_requests) >= self.max_rpd):
                return False
                
            # Add new request
            self.minute_requests.append(current_time)
            self.day_requests.append(current_time)
            self.tokens_per_minute += estimated_tokens
            return True
            
    def _cleanup_old_requests(self, current_time):
        minute_ago = current_time - timedelta(minutes=1)
        day_ago = current_time - timedelta(days=1)
        
        while self.minute_requests and self.minute_requests[0] < minute_ago:
            self.minute_requests.popleft()
            
        while self.day_requests and self.day_requests[0] < day_ago:
            self.day_requests.popleft()
            
        # Reset token count every minute
        if self.minute_requests and (current_time - self.minute_requests[0]).seconds >= 60:
            self.tokens_per_minute = 0
