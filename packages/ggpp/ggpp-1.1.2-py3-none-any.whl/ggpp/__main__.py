import os
import argparse


def run():
    # Program Description
    description = '''
    You can run your C/C++ code
    just passing the filename as first argument.
    Example:
    'ggpp targetfile.cpp'
    | You can also pass other arguments to the g++.
    Example:
    'ggpp targetfile.cpp -Wall -H'
    '''

    # Initialize Argument Parser
    parse = argparse.ArgumentParser(description=description)

    # Add arguments
    parse.add_argument('target_file', type=str, help='Target file to run.')
    parse.add_argument(
        '-c', '--clip', action='store_true', help='The file content will be copied to the clipboard. (xclip required)')
    parse.add_argument('-nr', '--noremove', action='store_true',
                       help='No remove the compiled file.')

    # Get all arguments
    args, unknown = parse.parse_known_args()

    # Get compiled name of the target file
    divisions = args.target_file.split('.')
    ext = divisions[len(divisions) - 1]
    compiled_name = args.target_file.replace('.' + ext, '')

    # Get all g++ args
    gpp_args = ''
    for arg in unknown:
        gpp_args += arg + ' '

    command = ''
    clip_command = ''

    # On Windows
    if os.name == 'nt':

        # Get the run command string
        command += "powershell.exe g++ {} -o {} ; ".format(args.target_file,
                                                           compiled_name) + gpp_args

        command += "{}.exe ; ".format(compiled_name)

        if not args.noremove:
            command += "rm -r {}.exe".format(compiled_name)

        # If "-c" or "--clip" exists, then run
        if args.clip:
            clip_command += "powershell.exe Get-Content {} | clip".format(
                args.target_file)

    # On Unix
    else:

        # Get the run command string
        command += "g++ {} -o {} && ".format(args.target_file,
                                             compiled_name) + gpp_args

        command += "./{} && ".format(compiled_name)

        if not args.noremove:
            command += "rm -rf {}".format(compiled_name)

        # If "-c" or "--clip" exists, then run
        if args.clip:
            clip_command += "xclip -selection clipboard {}".format(
                args.target_file)

    os.system(command)
    if args.clip:
        os.system(clip_command)


if __name__ == "__main__":
    run()
