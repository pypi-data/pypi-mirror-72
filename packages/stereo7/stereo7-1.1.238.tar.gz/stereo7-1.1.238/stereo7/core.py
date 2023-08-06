import os
import sys
from stereo7.project import Project
from stereo7 import fileutils
from stereo7 import ci_optimize_build
from stereo7 import validate
from stereo7 import compress_images
from stereo7 import create_sublime_project
from stereo7 import generate_android_project
from stereo7 import generate_xcode_project
from stereo7 import locales
from stereo7 import hockeyapp
from stereo7 import firebase_testlab
from stereo7 import version
from stereo7 import arguments
from stereo7 import inapps
from stereo7 import build


def console():
    main()


def _version():
    print(version.__version__)


def main():
    parser = arguments.Parser(sys.argv)
    command = parser.command

    fileutils.root_dir = os.path.abspath(parser.root)
    if not os.path.isdir(fileutils.root_dir):
        print('Invalid path to project [{}]'.format(parser.root))
        exit(-1)

    if command == 'init':
        project = Project(parser, empty=True)
        project.create()
        exit(0)
    if command == 'version':
        print(version.__version__)
        exit(0)

    Project.instance = Project(parser)

    if command == 'sublime':
        create_sublime_project.run()
    elif command == 'inapps_download':
        inapps.download_ios_metadata(Project.instance.apple_id)
    elif command == 'inapps':
        inapps.run(Project.instance.package,
                   Project.instance.name,
                   Project.instance.version,
                   Project.instance.gg_inapps,
                   parser)
    elif command == 'build':
        build.run(Project.instance.package,
                  Project.instance.version,
                  parser)
    elif command == 'robo-test':
        apk_path = parser.args['-binary_path']
        firebase_testlab.main(apk_path)
    elif command == 'gen-android':
        generate_android_project.run(parser)
    elif command == 'gen-ios':
        generate_xcode_project.run(parser)
    elif command == 'upload':
        build.upload(parser)
    elif command == 'upload_inapps':
        build.upload_inapps(parser)
    elif command == 'validate':
        validate.run()
    elif command == 'compress':
        compress_images.run(parser)
    elif command == 'locales':
        locales.download(Project.instance.gg_locales)
    elif command == 'create_locales_table':
        locales.convert_to_table()
    elif command == 'hockeyapp_upload':
        hockeyapp.hockey_app_upload(Project.instance, parser)
    elif command == 'appcenter_upload':
        hockeyapp.appcenter_upload(Project.instance, parser)
    elif command == 'ci_optimize_build':
        ci_optimize_build.main(Project.instance, parser)
    else:
        print('Unknown command [{}]'.format(command))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.extend('validate -r /Volumes/Elements/work/td_core/projects/steampunk/'.split(' '))
    main()
