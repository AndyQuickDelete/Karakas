import sys
from cx_Freeze import setup, Executable

company_name = 'Eastern Rising'
product_name = 'Karakas'

bdist_msi_options = {
    'upgrade_code': '{C715FF87-E996-3D95-9B37-CD0BBAC600FA}',
    'add_to_path': False,
    'all_users' : True,
    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
    'install_icon' : 'northstar.ico',
    }

build_exe_options = {
    'include_files': ['northstar.ico', 
                 'starsky.db', 
                 'optionDB',
                 'myfont.ttf'],
    'excludes': ['turtledemo', 'ctypes', 'test', 'dbm', 'venv'],
    }

# GUI applications require a different base on Windows
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

#icon = 'D:\\Source\\Python\\Karakas\\northstar.ico'

exe = Executable(script='karakas.py',
                 base=base,
                 icon='northstar.ico',
                 shortcut_name="Karakas",
                 shortcut_dir="ProgramMenuFolder",
                )

setup(name=product_name,
      version='1.0.2',
      description='Karakas Project Installer',
      executables=[exe],
      author='Andrew Evans',
      author_email='ade@rustytub.com',
      url = 'https://www.rustytub.com',
      options={
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options
          }
      )
