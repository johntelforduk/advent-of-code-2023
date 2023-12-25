# Advent of Code day 19, part 2, Aplenty.
# https://adventofcode.com/2023/day/19

from icecream import ic


def calc_product(ranges: dict) -> int:
    product = 1  # Work out the product of the 4 ranges.
    for c in ranges:
        l, u = ranges[c]
        product *= (u - l + 1)
    return product


def combinations(current_workflow: str,
                 current_rule_no: int,
                 ranges: dict,
                 workflows: dict) -> int:

    ic(current_workflow, current_rule_no)

    if current_workflow == 'A':
        return calc_product(ranges)

    if current_workflow == 'R':
        return 0

    current_rule = workflows[current_workflow][current_rule_no]

    if current_rule['operation'] == 'A':            # Accepted :)
        return calc_product(ranges)

    if current_rule['operation'] == 'R':            # Rejected :(
        return 0

    if current_rule['operation'] == 'goto':
        return combinations(current_workflow=current_rule['target'],
                            current_rule_no=0,
                            ranges=ranges, workflows=workflows)

    if current_rule['operation'] == '<':
        l, u = ranges[current_rule['category']]

        under_tuple = (l, min(u, current_rule['threshold'] - 1))
        over_tuple = (min(u, current_rule['threshold']), u)

        under_ranges = ranges.copy()
        over_ranges = ranges.copy()
        under_ranges[current_rule['category']] = under_tuple
        over_ranges[current_rule['category']] = over_tuple

        return (combinations(current_workflow=current_rule['target'],
                             current_rule_no=0,
                             ranges=under_ranges, workflows=workflows)
                + combinations(current_workflow=current_workflow,
                               current_rule_no=current_rule_no + 1,
                               ranges=over_ranges, workflows=workflows))

    if current_rule['operation'] == '>':
        l, u = ranges[current_rule['category']]

        under_tuple = (l, min(u, current_rule['threshold']))
        over_tuple = (min(u, current_rule['threshold']) + 1, u)

        under_ranges = ranges.copy()
        over_ranges = ranges.copy()
        under_ranges[current_rule['category']] = under_tuple
        over_ranges[current_rule['category']] = over_tuple

        return (combinations(current_workflow=current_rule['target'],
                             current_rule_no=0,
                             ranges=over_ranges, workflows=workflows)
                + combinations(current_workflow=current_workflow,
                               current_rule_no=current_rule_no + 1,
                               ranges=under_ranges, workflows=workflows))

        #     if categories[current_rule['category']] < current_rule['threshold']:
        #         if current_rule['target'] in 'AR':
        #             decision = current_rule['target']
        #         else:
        #             current_workflow = current_rule['target']
        #             current_rule_no = 0
        #     else:
        #         current_rule_no += 1
        #
        # elif current_rule['operation'] == '>':
        #     if categories[current_rule['category']] >= current_rule['threshold']:
        #         if current_rule['target'] in 'AR':
        #             decision = current_rule['target']
        #         else:
        #             current_workflow = current_rule['target']
        #             current_rule_no = 0
        #     else:
        #         current_rule_no += 1
        #
        # # elif current_rule['operation'] == 'goto':
        # #     current_workflow = current_rule['target']
        # #     current_rule_no = 0
        #
        # else:
        #     current_rule_no += 1
        #     current_rule = workflows[current_workflow].rules[current_rule_no]
        #
        # # if decision is None:
        # #     current_rule = workflows[current_workflow].rules[current_rule_no]
        #
        #


with open('test.txt', 'r') as file:
    input_str = file.read()

workflows_str, _ = input_str.split('\n\n')          # Don't need the Parts anymore.

# Key = workflow name. Value = workflow object.
workflows = {}

for description_str in workflows_str.split('\n'):
    name, rules_str = description_str.split('{')
    rules = []

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
            rules.append({'operation': operation,
                          'category': category,
                          'threshold': threshold,
                          'target': target})

        elif this_rule in 'AR':
            rules.append({'operation': this_rule})

        else:
            rules.append({'operation': 'goto',
                          'target': this_rule})

    workflows[name] = rules

ic(workflows)

ic(combinations(current_workflow='in',
                current_rule_no=0,
                ranges={'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)},
                workflows=workflows))
