class MetricsCalculator:
    def __init__(self):
        self.accuracy = 0
        self.precision = 0
        self.recall = 0
        self.f1_score = 0

        self.metrics = {
            'false_positive': 0,
            'false_negative': 0,
            'true_positive': 0,
            'true_negative': 0
        }
        self.single_vulnerability_metrics = {
            'access_control': 0,
            'arithmetic': 0,
            'denial_service': 0,
            'reentrancy': 0,
            'unchecked_low_calls': 0,
            'bad_randomness': 0,
            'front_running': 0,
            'time_manipulation': 0,
            'short_addresses': 0
        }
        self.right_vulnerability_found = {
            'found': 0,
            'total': 0
        }

    def get_metrics(self):
        return self.metrics

    def get_single_vuln_metrics(self):
        return self.single_vulnerability_metrics

    def update_metrics(self, metrics_obtained, single_vuln_metrics, vuln_found):
        self.metrics['false_positive'] += metrics_obtained['false_positive']
        self.metrics['false_negative'] += metrics_obtained['false_negative']
        self.metrics['true_positive'] += metrics_obtained['true_positive']
        self.metrics['true_negative'] += metrics_obtained['true_negative']
        self.right_vulnerability_found['found'] += vuln_found[0]
        self.right_vulnerability_found['total'] += vuln_found[1]
        self.single_vulnerability_metrics['access_control'] += single_vuln_metrics['access_control']
        self.single_vulnerability_metrics['arithmetic'] += single_vuln_metrics['arithmetic']
        self.single_vulnerability_metrics['denial_service'] += single_vuln_metrics['denial_service']
        self.single_vulnerability_metrics['reentrancy'] += single_vuln_metrics['reentrancy']
        self.single_vulnerability_metrics['unchecked_low_calls'] += single_vuln_metrics['unchecked_low_calls']
        self.single_vulnerability_metrics['bad_randomness'] += single_vuln_metrics['bad_randomness']
        self.single_vulnerability_metrics['front_running'] += single_vuln_metrics['front_running']
        self.single_vulnerability_metrics['time_manipulation'] += single_vuln_metrics['time_manipulation']
        self.single_vulnerability_metrics['short_addresses'] += single_vuln_metrics['short_addresses']

    def calculate_metrics(self):
        true_positives = self.metrics['true_positive']
        true_negatives = self.metrics['true_negative']
        false_negatives = self.metrics['false_negative']
        false_positives = self.metrics['false_positive']

        self.accuracy = (true_positives + true_negatives) / (
                true_positives + true_negatives + false_negatives + false_positives)

        self.precision = true_positives / (true_positives + false_positives)

        self.recall = true_positives / (true_positives + false_negatives)

        self.f1_score = 2 * (self.precision * self.recall) / (self.precision + self.recall)

    def stamp_metrics(self):
        print(f"\nTotal Metrics:")
        print(
            f"Total vulnerabilities found: {self.right_vulnerability_found['found']}/{self.right_vulnerability_found['total']}")
        print(f'True positives: {self.metrics["true_positive"]}')
        print(f'True negatives: {self.metrics["true_negative"]}')
        print(f'False positives: {self.metrics["false_negative"]}')
        print(f'False negatives: {self.metrics["false_positive"]}')
        print(f'Accuracy: {self.accuracy}')
        print(f'Precision: {self.precision}')
        print(f'Recall: {self.recall}')
        print(f'F1 Score: {self.f1_score}')
        for single_vulnerability_metric in self.single_vulnerability_metrics:
            print(f'{single_vulnerability_metric}: {self.single_vulnerability_metrics[single_vulnerability_metric]}')
