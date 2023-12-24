# Advent of Code day 19, Aplenty.
# https://adventofcode.com/2023/day/19

from icecream import ic


class Workflow:

    def __init__(self, description_str: str):
        self.name, rules_str = description_str.split('{')

        self.rules = []
        for this_rule in rules_str.replace('}', '').split(','):

            if '<' in this_rule or '>' in this_rule:
                if '<' in this_rule:
                    operation = '<'
                    category, rest = this_rule.split('<')
                else:
                    operation = '>'
                    category, rest = this_rule.split('>')
                threshold_str, target = rest.split(':')
                threshold = int(threshold_str)
                self.rules.append({'operation': operation,
                              'category': category,
                              'threshold': threshold,
                              'target': target})

            elif this_rule in 'AR':
                self.rules.append({'operation': this_rule})

            else:
                self.rules.append({'operation': 'goto',
                                   'target': this_rule})


class Part:

    def __init__(self, description_str: str):
        description = description_str.replace('{', '').replace('}','')
        self.categories = {}
        for each_term in description.split(','):
            category, value_str = each_term.split('=')
            self.categories[category] = int(value_str)


with open('input.txt', 'r') as file:
    input_str = file.read()

workflows_str, parts_str = input_str.split('\n\n')

# Key = workflow name. Value = workflow object.
workflows = {}

for description in workflows_str.split('\n'):
    new_workflow = Workflow(description)
    workflows[new_workflow.name] = new_workflow

total = 0
for part_str in parts_str.split('\n'):
    part = Part(part_str)

    current_workflow = 'in'
    current_rule_no = 0
    current_rule = workflows[current_workflow].rules[current_rule_no]
    decision = None

    while decision is None:
        if current_rule['operation'] == '<':
            if part.categories[current_rule['category']] < current_rule['threshold']:
                if current_rule['target'] in 'AR':
                    decision = current_rule['target']
                else:
                    current_workflow = current_rule['target']
                    current_rule_no = 0
            else:
                current_rule_no += 1

        elif current_rule['operation'] == '>':
            if part.categories[current_rule['category']] > current_rule['threshold']:
                ic(current_rule['target'])
                if current_rule['target'] in 'AR':
                    decision = current_rule['target']
                else:
                    current_workflow = current_rule['target']
                    current_rule_no = 0
            else:
                current_rule_no += 1

        elif current_rule['operation'] == 'goto':
            current_workflow = current_rule['target']
            current_rule_no = 0

        elif current_rule['operation'] in 'AR':
            decision = current_rule['operation']
        else:
            current_rule_no += 1
            current_rule = workflows[current_workflow].rules[current_rule_no]

        if decision is None:
            current_rule = workflows[current_workflow].rules[current_rule_no]

        ic(current_workflow, current_rule_no, decision)

    if decision == 'A':
        for this_category in part.categories:
            total = total + part.categories[this_category]

ic(total)
