from parse_vulnerability import strip_vulnerability

right_vulnerability_found = {
    'access_control': 0,
    'arithmetic': 0,
    'denial_service': 0,
    'reentrancy': 0,
    'unchecked_low_calls': 0,
    'bad_randomness': 0,
    'front_running': 0,
    'time_manipulation': 0,
    'short_addresses': 0,
    'total': 0
}


class MetricsCalculator:
    def __init__(self):
        self.found = 0
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

    def get_metrics(self):
        return self.metrics

    def get_single_vuln_metrics(self):
        return self.single_vulnerability_metrics

    def update_metrics(self, metrics_obtained, single_vuln_metrics, vuln_found):
        self.found += vuln_found
        for key in metrics_obtained.keys():
            self.metrics[key] += metrics_obtained[key]
        for key in single_vuln_metrics.keys():
            self.single_vulnerability_metrics[key] += single_vuln_metrics[key]

    def calculate_metrics(self):
        true_positives = self.metrics['true_positive']
        true_negatives = self.metrics['true_negative']
        false_negatives = self.metrics['false_negative']
        false_positives = self.metrics['false_positive']

        self.accuracy = (true_positives + true_negatives) / (
                true_positives + true_negatives + false_negatives + false_positives)

        self.precision = true_positives / (true_positives + false_positives)

        self.recall = true_positives / (true_positives + false_negatives)

        if self.precision > 0 or self.precision > 0:
            self.f1_score = 2 * (self.precision * self.recall) / (self.precision + self.recall)
        else:
            self.f1_score = 0

    def stamp_metrics(self, tool_name):
        print(f"\nTotal vulnerabilities found by {tool_name}: {self.found}/"
              f"{right_vulnerability_found['total']}")
        print(f'True positives: {self.metrics["true_positive"]}')
        print(f'True negatives: {self.metrics["true_negative"]}')
        print(f'False negatives: {self.metrics["false_negative"]}')
        print(f'False positives: {self.metrics["false_positive"]}')
        print(f'Accuracy: {self.accuracy}')
        print(f'Precision: {self.precision}')
        print(f'Recall: {self.recall}')
        print(f'F1 Score: {self.f1_score}')
        for single_vulnerability_metric in self.single_vulnerability_metrics:
            print(f'{single_vulnerability_metric}: {self.single_vulnerability_metrics[single_vulnerability_metric]}/'
                  f'{right_vulnerability_found[single_vulnerability_metric]}')


def total_vulnerabilities_counter(artifact):
    for key in right_vulnerability_found.keys():
        right_vulnerability_found[key] = 0

    for row in artifact:
        artifact_vulnerabilities = strip_vulnerability(row['tag'])
        for vuln in artifact_vulnerabilities:
            vuln_name = vuln[1]
            if vuln_name != 'other' and vuln_name != 'no':
                right_vulnerability_found[vuln_name] += 1

    total_vulnerabilities = 0
    for row in artifact:
        row_vuln = row['tag']
        if ';' in row_vuln:
            elements = row_vuln.split(';')
            if 'no' in elements:
                print(row_vuln)
            else:
                total_vulnerabilities += len(elements) - 1
    right_vulnerability_found['total'] = total_vulnerabilities
