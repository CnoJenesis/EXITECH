class RFIDReader:
    def __init__(self):
        self.running = False
        self.thread = None
        self.callback = None
        self.last_scan = None
        self.last_scan_time = None
        from datetime import datetime
        self.last_scan_time = datetime.now()

    def set_callback(self, callback):
        self.callback = callback

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def process_card(self, card_id):
        if card_id:
            # Store the last scan
            self.last_scan = card_id.strip()
            
            # Update the timestamp
            from datetime import datetime
            self.last_scan_time = datetime.now()
            
            # Call the callback if set
            if self.callback:
                self.callback(self.last_scan)
    
    def get_last_scan(self):
        """
        Returns the last RFID scan value if it's recent (within 5 seconds)
        """
        if not self.last_scan:
            return None
            
        # Check if the scan is recent
        from datetime import datetime, timedelta
        now = datetime.now()
        
        # Only return scans from the last 5 seconds
        if now - self.last_scan_time < timedelta(seconds=5):
            return self.last_scan
        
        return None
        
    def clear_last_scan(self):
        """
        Clears the last scan data
        """
        self.last_scan = None