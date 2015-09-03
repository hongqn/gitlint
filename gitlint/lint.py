from __future__ import print_function
from gitlint import rules


class GitLinter(object):
    def __init__(self, config):
        self.config = config

    @property
    def body_line_rules(self):
        return [rule for rule in self.config.body_rules if isinstance(rule, rules.LineRule)]

    @property
    def title_line_rules(self):
        return [rule for rule in self.config.title_rules if isinstance(rule, rules.LineRule)]

    def _apply_line_rules(self, lines, rules, line_nr_start):
        """ Iterates over the lines in a given git commit message and applies all the enabled line rules to
        each line """
        all_violations = []
        line_nr = line_nr_start
        for line in lines:
            for rule in rules:
                violation = rule.validate(line)
                if violation:
                    violation.line_nr = line_nr
                    all_violations.append(violation)
            line_nr += 1
        return all_violations

    def lint_commit_message(self, commit_message):
        lines = commit_message.split("\n")
        commit_message_title = [lines[0]]
        commit_message_body = lines[1:] if len(lines) > 1 else []
        title_violations = self._apply_line_rules(commit_message_title, self.title_line_rules, 1)
        body_violations = self._apply_line_rules(commit_message_body, self.body_line_rules, 2)
        violations = title_violations + body_violations
        for v in violations:
            print("{}: {} {}: \"{}\"".format(v.line_nr, v.rule_id, v.message, v.content))
        return len(violations)
