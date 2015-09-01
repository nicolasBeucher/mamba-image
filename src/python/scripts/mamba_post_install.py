# Mamba image library post-installation script

import sys
import os
import shutil

def findMambaShellPath():
    # Retrieves the path to the mambaShell script and to its icon
    # Returns them in a tuple. (empty if unsuccessful).
    #
    # Use this instead of the classic __file__ method because import 
    # behaves erratically when inside the installer.
    for pdir in sys.path:
        if os.path.isdir(pdir):
            l = os.listdir(pdir)
            if l.count('mambaShell'):
                mbShellPath = os.path.join(pdir, 'mambaShell'+os.path.sep+'__init__.py')
                iconPath = os.path.join(pdir, 'mambaShell'+os.path.sep+'mamba.ico')
                return (mbShellPath, iconPath)
                
    return ('','')

if sys.argv[1]=="-install":
    print("mamba post-installation script [INSTALL]")

    try:
        (mbShellPath, iconPath) = findMambaShellPath()
        if mbShellPath!='':
            import idlelib
            # Creation of a subdirectory in the start menu
            menu_path = get_special_folder_path("CSIDL_PROGRAMS")
            dir_path = os.path.join(menu_path,'Mamba Image')
            os.mkdir(dir_path)
            directory_created(dir_path)
            
            # Creation of the shortcut in the subdirectory
            arguments = os.path.join(os.path.dirname(idlelib.__file__), 'idle.pyw')
            arguments += ' -n -i -t "Python Shell (Mamba specific IDLE)" -c '
            arguments += ' "from mambaShell import *"'
            short_name = "Mamba Shell.lnk"
            create_shortcut(
                os.path.join(sys.prefix, "pythonw.exe"),
                "Mamba Shell",
                short_name,
                arguments,
                '',
                iconPath
            )
            # Move shortcut to the subdirectory
            shutil.move(os.path.join(os.getcwd(), short_name),
                        os.path.join(dir_path, short_name))
            file_created(os.path.join(dir_path, short_name))
        else:
            print("Could not find the mambaShell, please verify your installation")
    except ImportError:
        print("IDLE not present on you computer or Mamba installation error : abort")

elif sys.argv[1]=="-remove":
    print("Mamba post-installation script [REMOVE]")

else:
    print("Mamba post-installation script error")
