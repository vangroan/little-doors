import os
from shutil import copyfile

import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--art-dir', default='./art', help="Relative path to art assets")
@click.option('--resource-dir', default='./resources', help="Relative path to target resources directory")
def assets(art_dir, resource_dir):
    """
    Copies assets into the resources directory so they can be shipped.
    """
    extensions = ['png']
    print("Searching %s for files with extensions: %s " % (art_dir, extensions))

    for root, directories, files in os.walk(art_dir):
        for filename in files:
            ext = filename.split('.')[1:]
            if ext:
                if ext[0] in extensions:
                    # Do Copy
                    src = os.path.normpath(os.path.join(root, filename))
                    dst_dir = os.path.join(resource_dir, root)
                    dst = os.path.normpath(os.path.join(dst_dir, filename))

                    # Ensure Resources directory exists
                    os.makedirs(dst_dir, exist_ok=True)

                    print("Copying %s to %s" % (src, dst))
                    copyfile(src, dst)


if __name__ == '__main__':
    cli()
