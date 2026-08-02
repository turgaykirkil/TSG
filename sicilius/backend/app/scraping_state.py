import threading

class ScrapingState:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.is_running = False
            self.is_paused = False
            self.should_stop = False
            self.processed = 0
            self.total = 0
            self.pdf_size = 0  # Placeholder from frontend
            self.companies = []
            self.error_message = None
            self.logs = []
            self.last_sicil_no = None

    def start(self, total_count):
        with self.lock:
            self.is_running = True
            self.is_paused = False
            self.should_stop = False
            self.processed = 0
            self.total = total_count
            self.companies = []
            self.error_message = None
            self.logs = []

    def pause(self):
        with self.lock:
            self.is_paused = True

    def resume(self):
        with self.lock:
            self.is_paused = False

    def stop(self):
        with self.lock:
            self.should_stop = True
            self.is_paused = False

    def set_last_sicil_no(self, sicil_no: int):
        with self.lock:
            self.last_sicil_no = sicil_no

    def add_company_result(self, company_data):
        with self.lock:
            self.processed += 1
            # Avoid duplicates, update if exists
            existing = next((c for c in self.companies if c['id'] == company_data['id']), None)
            if existing:
                existing.update(company_data)
            else:
                self.companies.insert(0, company_data) # Add to the beginning

    def set_error(self, message):
        with self.lock:
            self.error_message = message
            self.is_running = False
            self.is_paused = False

    def finish(self):
        with self.lock:
            self.is_running = False
            self.is_paused = False

    def add_log(self, message):
        print(f"[SCRAPER] {message}", flush=True)
        with self.lock:
            self.logs.append(message)

    def update_progress(self, processed: int):
        with self.lock:
            try:
                p = int(processed)
            except Exception:
                p = self.processed
            self.processed = max(0, p)

    def get_status(self):
        with self.lock:
            return {
                "running": self.is_running,
                "paused": self.is_paused,
                "processed": self.processed,
                "total": self.total,
                "error": self.error_message,
                "logs": self.logs,
                "companies": self.companies,
                "last_sicil_no": self.last_sicil_no,
            }

# Singleton instance to share state across the application
scraping_state = ScrapingState()
