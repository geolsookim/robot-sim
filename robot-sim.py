import argparse


class RobotSim(object):
    LEFT = {
        'NORTH': 'WEST',
        'WEST': 'SOUTH',
        'SOUTH': 'EAST',
        'EAST': 'NORTH',
    }

    RIGHT = {
        'NORTH': 'EAST',
        'EAST': 'SOUTH',
        'SOUTH': 'WEST',
        'WEST': 'NORTH',
    }

    def __init__(self):
        self.current_location = {}

    def find_first_place_command(self, command_inputs: list):
        place_indices = [i for i,c in enumerate(command_inputs) if c.startswith('PLACE')]
        if place_indices:
            index = place_indices.pop(0)
            for command in command_inputs[:index]:
                print(command)
            return command_inputs[index:]
        else:
            return None

    def get_next_location(self, command: str):
        if command.startswith('PLACE'):
            coordinates = command.split()[1].split(',')
            return {
                'X': int(coordinates[0]),
                'Y': int(coordinates[1]),
                'F': coordinates[2],
            }
        elif command == 'MOVE':
            X = self.current_location['X']
            Y = self.current_location['Y']
            F = self.current_location['F']
            if F == 'NORTH':
                Y += 1
            elif F == 'SOUTH':
                Y += -1
            elif F == 'EAST':
                X += 1
            elif F == 'WEST':
                X += -1
            return {'X': X, 'Y': Y, 'F': F}

    def is_valid_location(self, location: dict):
        X = location.get('X')
        Y = location.get('Y')
        F = location.get('F')
        return location and (0 <= X < 5) and (0 <= Y < 5)

    def run(self, command_inputs: list):
        # "The first valid command to the robot is a PLACE command"
        command_list = self.find_first_place_command(command_inputs)

        if not command_list:
            for command in command_inputs:
                print(command)
            return

        while True:
            try:
                command = command_list.pop(0)
            except (AttributeError, IndexError):
                break

            print(command)
            # "The application should discard all commands in the sequence until a valid PLACE command has been executed."
            if not self.current_location and not command.startswith('PLACE'):
                continue

            if command == 'MOVE' or command.startswith('PLACE'):
                next_location = self.get_next_location(command)
                if self.is_valid_location(next_location):
                    self.current_location = next_location
                else:
                    continue

            elif command == 'LEFT':
                F = self.current_location['F']
                self.current_location['F'] = self.LEFT[F]

            elif command == 'RIGHT':
                F = self.current_location['F']
                self.current_location['F'] = self.RIGHT[F]

            elif command == 'REPORT':
                X = self.current_location['X']
                Y = self.current_location['Y']
                F = self.current_location['F']
                print(f"Output: {X},{Y},{F}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command_file", help="file containing a list of commands")
    args = parser.parse_args()

    try:
        command_inputs = [line.rstrip('\n') for line in open(args.command_file)]
    except FileNotFoundError as e:
        print(f"File '{args.command_file}' not found. Exiting.")
    else:
#        import pdb;pdb.set_trace()
        sim = RobotSim()
        sim.run(command_inputs)
