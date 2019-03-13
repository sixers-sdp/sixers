is_north = {
    'NORTH': 'FORWARD',
    'SOUTH': 'BACKWARDS',
    'EAST': 'RIGHT',
    'WEST': 'LEFT'
}

is_south = {
    'NORTH': 'BACKWARDS',
    'SOUTH': 'FORWARD',
    'EAST': 'LEFT',
    'WEST': 'RIGHT'
}

is_east = {
    'NORTH': 'LEFT',
    'SOUTH': 'RIGHT',
    'EAST': 'FORWARD',
    'WEST': 'BACKWARDS'
}

is_west = {
    'NORTH': 'RIGHT',
    'SOUTH': 'LEFT',
    'EAST': 'BACKWARDS',
    'WEST': 'FORWARD'
}

conversion_table = {
    'NORTH': is_north,
    'SOUTH': is_south,
    'EAST': is_east,
    'WEST': is_west,
}



orientation_change_north = {
    'RIGHT': 'EAST',
    'LEFT': 'WEST',
    'BACKWARDS': 'SOUTH',
    'FORWARD': 'NORTH',
}

orientation_change_south = {
    'RIGHT': 'WEST',
    'LEFT': 'EAST',
    'BACKWARDS': 'NORTH',
    'FORWARD': 'SOUTH',
}

orientation_change_east = {
    'RIGHT': 'SOUTH',
    'LEFT': 'NORTH',
    'BACKWARDS': 'WEST',
    'FORWARD': 'EAST',
}

orientation_change_west = {
    'RIGHT': 'NORTH',
    'LEFT': 'SOUTH',
    'BACKWARDS': 'EAST',
    'FORWARD': 'WEST',
}

orientation_conversion_table = {
    'NORTH': orientation_change_north,
    'SOUTH': orientation_change_south,
    'EAST': orientation_change_east,
    'WEST': orientation_change_west,
}


CURRENT_ORIENTATION = 'NORTH'


def convert_plan_to_relative_orientation(plan):
    global CURRENT_ORIENTATION

    plan_changed = []

    for task in plan.plan_generated['steps']:
        action = task['action']
        if action != 'MOVE':
            plan_changed.append(task)

        direction = task['args']['direction']
        converted = conversion_table[CURRENT_ORIENTATION][direction]

        CURRENT_ORIENTATION = orientation_conversion_table[CURRENT_ORIENTATION][converted]
        task['relative_orientation'] = converted