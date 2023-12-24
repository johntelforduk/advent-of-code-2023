# Advent of Code day 19, part 2, Aplenty.
# https://adventofcode.com/2023/day/19

from icecream import ic


class Workflow:

    def __init__(self, description_str: str):
        self.name, rules_str = description_str.split('{')

        self.rules = []

        self.thresholds = {}
        for c in 'xmas':
            self.thresholds[c] = set()
            self.thresholds[c].add(1)
            self.thresholds[c].add(4001)

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
                self.thresholds[category].add(threshold)

            elif this_rule in 'AR':
                self.rules.append({'operation': this_rule})

            else:
                self.rules.append({'operation': 'goto',
                                   'target': this_rule})


# class Part:
#
#     def __init__(self, description_str: str):
#         description = description_str.replace('{', '').replace('}','')
#         self.categories = {}
#         for each_term in description.split(','):
#             category, value_str = each_term.split('=')
#             self.categories[category] = int(value_str)

def pairs(my_list: list) -> list:
    my_pairs = list()
    i = 0
    a = my_list[i]
    while i < len(my_list) - 1:
        i += 1
        b = my_list[i]
        my_pairs.append((a, b - 1))
        a = b
    return my_pairs


def is_accepted(categories: dict, workflows: dict) -> bool:
    current_workflow = 'in'
    current_rule_no = 0
    current_rule = workflows[current_workflow].rules[current_rule_no]
    decision = None

    while decision is None:
        if current_rule['operation'] == '<':
            if categories[current_rule['category']] < current_rule['threshold']:
                if current_rule['target'] in 'AR':
                    decision = current_rule['target']
                else:
                    current_workflow = current_rule['target']
                    current_rule_no = 0
            else:
                current_rule_no += 1

        elif current_rule['operation'] == '>':
            if categories[current_rule['category']] >= current_rule['threshold']:
                # ic(current_rule['target'])
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

        # ic(current_workflow, current_rule_no, decision)

    # ic(decision)
    if decision == 'A':
        return True
    else:
        return False


with open('test.txt', 'r') as file:
    input_str = file.read()

workflows_str, parts_str = input_str.split('\n\n')

# Key = workflow name. Value = workflow object.
workflows = {}

thresholds = {}
for c in 'xmas':
    thresholds[c] = set()

for description in workflows_str.split('\n'):
    new_workflow = Workflow(description)
    # ic(new_workflow.name, new_workflow.thresholds)

    for c in 'xmas':
        thresholds[c] = thresholds[c].union(new_workflow.thresholds[c])

    workflows[new_workflow.name] = new_workflow

# total = 0
# for part_str in parts_str.split('\n'):
#     part = Part(part_str)

# part = Part('{x=1679,m=44,a=2067,s=496}')
# ic(is_accepted(part, workflows))


ic(thresholds)

thresholds_lists = {}
for c in thresholds:
    as_list = list(thresholds[c])
    as_list.sort()
    thresholds_lists[c] = as_list

ic(thresholds_lists)

ic(is_accepted({'x': 1, 'm': 1, 'a': 1, 's': 1}, workflows))
ic(is_accepted({'x': 1416, 'm': 838, 'a': 1716, 's': 537}, workflows))

ic(pairs(thresholds_lists['s']))

total = 0
for x1, x2 in pairs(thresholds_lists['x']):
    for m1, m2 in pairs(thresholds_lists['m']):
        for a1, a2 in pairs(thresholds_lists['a']):
            for s1, s2 in pairs(thresholds_lists['s']):
                if is_accepted({'x': x1, 'm': m1, 'a': a1, 's': s1}, workflows):
                    size = (x2 - x1 + 1) * (m2 - m1 + 1) * (a2 - a1 + 1) * (s2 - s1 + 1)
                    ic('accepted')
                    total += size
                else:
                    ic('not accepted')

ic(total)


# 167409079868000
# 167474394229030

# [1, 10, 15, 20] = 20 numbers
# (1, 9), (10, 14), (15, 20)
# 9 + 5 + 6 = 20


# 167474394229030
