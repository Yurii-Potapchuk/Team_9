import difflib
import inspect
import functools



# example
def input_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError,TypeError) as e:
            if "takes" in str(e) and "but" in str(e):
                error_message = "Too many arguments provided"
                return error_message
            else:
                error_message = str(e).split(':')[1]
                return f"Give me {error_message}"
    return wrapper


# example
@input_errors
def add(name:str, phone:str):
    ...


# example
@input_errors
def change():
    ...


# example
command_dict = {
    'add': [add, 'add contact'],
    'change': [change, 'change existing contact']
}


# use difflib.get_close_matches for guess the command. Usually cutoff=0.6, but maybe better to set 0.4-0.5 to wider guessing
def command_handler(user_input, command_dict):
    if user_input in command_dict:
        return command_dict[user_input][0]
    possible_command = difflib.get_close_matches(user_input.split()[0], command_dict, cutoff=0.45)
    if possible_command:
        return f'An unknown command. Maybe you mean: {", ".join(possible_command)}'
    else:
        return f'An unknown command.'


# like welcome message - to show all funcs for contact book etc. 
def instruction (command_dict):
    result = []
    for func_name, func in command_dict.items():
        signature = inspect.signature(func[0])
        parameters = signature.parameters
        param_names = ' '.join(parameters.keys())

        if 'args' in parameters or 'kwargs' in parameters:
            result.append('{:<20s} {:<30s} {:s}'.format(func_name, "", func[1]))
        else:
            result.append('{:<20s} {:<30s} {:s}'.format(func_name, f"{param_names if param_names else ''}", func[1]))

    headers = '{:<20s} {:<30s} {:s}'.format('Command', 'Parameters', 'Description')
    rows_command = headers + '\n' + '\n'.join(result)
    
    return rows_command.strip('\n')


# example of parser user_input
def parser_input(user_input: str, command_dict) -> tuple():
    command = None
    arguments = ''

    for key in command_dict.keys():
        if user_input.startswith(key):
            command = key
            arguments = user_input.replace(key, '').strip().split()
            break
    return command, arguments


if __name__ == "__main__":
    while True:
        user_input = input('>>> ').lower()
        if user_input == 'menu' or user_input == 'start':     # input 'menu' or 'start' to show all funcs
            print("How can I help you?\n")
            print(instruction(command_dict))
        elif user_input in ('good bye', "close", "exit"):
            # del_file_if_empty()
            print('Good bye!')
            break
        else:
            command, arguments = parser_input(user_input, command_dict)
            if command in command_dict:
                result = command_handler(command, command_dict)(*arguments)
            else:
                result = command_handler(user_input, command_dict)
            print(result)