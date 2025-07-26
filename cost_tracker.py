import json
import os
from datetime import datetime, timedelta

class CostTracker:
    USAGE_FILE = "usage_data.json"
    DAILY_LIMIT = 50.0  # USD
    MONTHLY_LIMIT = 200.0  # USD

    # GPT-4o-mini pricing per 1 million tokens
    INPUT_COST_PER_MILLION_TOKENS = 0.15
    OUTPUT_COST_PER_MILLION_TOKENS = 0.60

    def __init__(self):
        self.usage_data = self._load_usage_data()

    def _load_usage_data(self):
        if os.path.exists(self.USAGE_FILE):
            with open(self.USAGE_FILE, 'r') as f:
                return json.load(f)
        return {"daily": {}, "monthly": {}}

    def _save_usage_data(self):
        with open(self.USAGE_FILE, 'w') as f:
            json.dump(self.usage_data, f, indent=4)

    def _get_current_date(self):
        return datetime.now().strftime("%Y-%m-%d")

    def _get_current_month(self):
        return datetime.now().strftime("%Y-%m")

    def record_usage(self, input_tokens: int, output_tokens: int):
        cost = self._calculate_cost(input_tokens, output_tokens)
        current_date = self._get_current_date()
        current_month = self._get_current_month()

        if current_date not in self.usage_data["daily"]:
            self.usage_data["daily"][current_date] = 0.0
        self.usage_data["daily"][current_date] += cost

        if current_month not in self.usage_data["monthly"]:
            self.usage_data["monthly"][current_month] = 0.0
        self.usage_data["monthly"][current_month] += cost

        self._save_usage_data()
        return cost

    def _calculate_cost(self, input_tokens: int, output_tokens: int):
        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION_TOKENS
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION_TOKENS
        return input_cost + output_cost

    def get_daily_usage(self):
        self._clean_old_daily_data()
        return self.usage_data["daily"].get(self._get_current_date(), 0.0)

    def get_monthly_usage(self):
        self._clean_old_monthly_data()
        return self.usage_data["monthly"].get(self._get_current_month(), 0.0)

    def _clean_old_daily_data(self):
        # Remove daily data older than 31 days
        today = datetime.now()
        dates_to_keep = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(31)]
        self.usage_data["daily"] = {date: cost for date, cost in self.usage_data["daily"].items() if date in dates_to_keep}
        self._save_usage_data()

    def _clean_old_monthly_data(self):
        # Remove monthly data older than 12 months
        current_month_dt = datetime.strptime(self._get_current_month(), "%Y-%m")
        months_to_keep = [(current_month_dt - timedelta(days=30*i)).strftime("%Y-%m") for i in range(12)]
        self.usage_data["monthly"] = {month: cost for month, cost in self.usage_data["monthly"].items() if month in months_to_keep}
        self._save_usage_data()

    def can_afford(self, estimated_cost: float):
        daily_remaining = self.DAILY_LIMIT - self.get_daily_usage()
        monthly_remaining = self.MONTHLY_LIMIT - self.get_monthly_usage()

        return estimated_cost <= daily_remaining and estimated_cost <= monthly_remaining

    def get_remaining_budget(self):
        daily_remaining = self.DAILY_LIMIT - self.get_daily_usage()
        monthly_remaining = self.MONTHLY_LIMIT - self.get_monthly_usage()
        return daily_remaining, monthly_remaining
