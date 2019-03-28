

def group_plan(plan):
    """
    Move tasks are special - we should execute all following moves at once
    """
    groups = []

    current_group = None
    current_tasks = []
    for step in plan['steps']:
        action = step['action']
        print(action)
        if current_group is None:
            current_group = action

        if current_group == action:
            current_tasks.append(step)
        else:
            groups.append(current_tasks)
            current_group = action
            current_tasks = [step]

    groups.append(current_tasks)
    return groups
