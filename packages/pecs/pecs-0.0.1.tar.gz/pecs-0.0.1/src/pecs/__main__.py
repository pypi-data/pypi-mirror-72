import argparse
from .supported_command import Command
from .generate import generate
from pecs import VERSION

def header():
    return """      ___           ___           ___           ___     
     /\  \         /\  \         /\  \         /\  \    
    /::\  \       /::\  \       /::\  \       /::\  \   
   /:/\:\  \     /:/\:\  \     /:/\:\  \     /:/\ \  \  
  /::\~\:\  \   /::\~\:\  \   /:/  \:\  \   _\:\~\ \  \ 
 /:/\:\ \:\__\ /:/\:\ \:\__\ /:/__/ \:\__\ /\ \:\ \ \__\ 
 \/__\:\/:/  / \:\~\:\ \/__/ \:\  \  \/__/ \:\ \:\ \/__/
      \::/  /   \:\ \:\__\    \:\  \        \:\ \:\__\  
       \/__/     \:\ \/__/     \:\  \        \:\/:/  /  
                  \:\__\        \:\__\        \::/  /   
                   \/__/         \/__/         \/__/    """

def main(argv=None):
    parser = argparse.ArgumentParser(description='The pecs autogenerator utility')
    parser.add_argument(
        'command',
        help='The action to execute. Current valid values: [\'generate\']'
    )
    parser.add_argument(
        '--dburl',
        dest='dburl',
        required=True,
        help='The database connection string (example: postgresql://user:pass@localhost:5432/my_db)',
    )
    args = parser.parse_args()

    command = Command(args.command)

    print(header())
    print(f'Version {VERSION}')
    if command == Command.GENERATE:
        generate(args.dburl)

if __name__ == '__main__':
    main()
