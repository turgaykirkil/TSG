import threading

class ScrapingState:
    def __init__(self):
        self.lock = threading.Lock()
        self.reset()

    def reset(self):
        with self.lock:
            self.is_running = False
            self.should_stop = False
            self.processed = 0
            self.total = 0
            self.pdf_size = 0  # Placeholder from frontend
            self.companies = []
            self.error_message = None
            self.logs = []

    def start(self, total_count):
        with self.lock:
            self.is_running = True
            self.should_stop = False
            self.processed = 0
            self.total = total_count
            self.companies = []
            self.error_message = None
            self.logs = []

    def stop(self):
        with self.lock:
            self.should_stop = True

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

    def finish(self):
        with self.lock:
            self.is_running = False

    def add_log(self, message):
        with self.lock:
            self.logs.append(message)

    def get_status(self):
        with self.lock:
            return {
                "running": self.is_running,
                "processed": self.processed,
                "total": self.total,
                "error": self.error_message,
                "logs": self.logs,
                "companies": self.companies,
            }

# Singleton instance to share state across the application
scraping_state = ScrapingState()
