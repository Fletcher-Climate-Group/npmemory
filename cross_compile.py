"""
Copyright © 2020 Daniel Hogg

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Cross-compilation

Linux: gcc v8
Windows: gcc TDM 64
https://jmeubank.github.io/tdm-gcc/
Mac: gcc?
"""

import os
import glob
import shutil
import subprocess

WINDOWS_COMPILER = "C:\\TDM-GCC-64\\bin\\gcc.exe"

def empty_folder(folder):

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_package_name():

    pkgs = glob.glob("*.whl")

    if len(pkgs) != 1:
        raise ValueError("Multiple packages in dist.")

    return pkgs[0]


def win_compile(directory, mod_name):
    # Cleanup and build for windows

    if not os.path.isfile(WINDOWS_COMPILER):
        msg = f"Windows compiler not found: {WINDOWS_COMPILER}. Please specify a compiler."
        raise FileNotFoundError(msg)

    os.chdir(directory)
    o_file = os.path.join(directory, mod_name + ".o")
    dll_file = os.path.join(directory, mod_name + ".dll")

    if os.path.isfile(o_file):
        os.remove(o_file)

    if os.path.isfile(dll_file):
        os.remove(dll_file)

    obj_cmd = f"{WINDOWS_COMPILER} -c -o {mod_name}.o {mod_name}.c"
    dll_cmd = f"{WINDOWS_COMPILER} -o {mod_name}.dll -s -shared {mod_name}.o -Wl,--subsystem,windows"

    subprocess.call(obj_cmd)
    subprocess.call(dll_cmd)


def rebuild():

    base_dir = os.getcwd()

    clibs_dir = os.path.join(base_dir, "npmemory", "clibs")

    if not os.path.isdir("./build"):
        os.mkdir("./build")
    
    if not os.path.isdir("./dist"):
        os.mkdir("./dist")

    empty_folder("./build")
    empty_folder("./dist")

    # Cross-compilation

    if os.name == 'posix':
        os.chdir(clibs_dir)
        subprocess.call("make")
    elif os.name == 'nt':
        win_compile(clibs_dir, "box_average")
    else:
        raise OSError(f"OS not supported: {os.name}")

    os.chdir(base_dir)

    subprocess.call("python setup.py bdist_wheel", shell=True)
    os.chdir("./dist")

    pkg_name = get_package_name()
    print(pkg_name)
    
    subprocess.call(f"pip uninstall -y {pkg_name}", shell=True)
    subprocess.call(f"pip install {pkg_name}", shell=True)

    print(f"Package installed: {pkg_name}")


rebuild()
