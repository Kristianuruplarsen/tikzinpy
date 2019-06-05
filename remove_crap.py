
'''
This just removes all files that are from building the latex documents
'''

import os
import click


@click.command()
@click.argument('directory', default='notebooks/test/', type = click.Path(exists=True))
def remove(directory):
        content = os.listdir(directory)
        for item in content:
                if item.endswith(('.log', '.aux', '.gz', '.fdb_latexmk', '.fls', '.tex')):
                        click.echo(f"Removed {directory + item}")
                        os.remove(directory + item)                     
                        

if __name__ == '__main__':
        remove()