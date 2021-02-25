"""
Offers classes and functions.
Offers access to the Virtual File Server (VFS) which you can use to manipulate files and folders.
"""
# Standard Library Imports
import shutil
import os

# Other imports
from addondev.utils import safe_path, ensure_native_str
from addondev.support import kodi_paths

__author__ = 'Team Kodi <http://kodi.tv>'
__credits__ = 'Team Kodi'
__date__ = 'Fri May 01 16:22:23 BST 2015'
__platform__ = 'ALL'
__version__ = '2.25.0'


def copy(source, destination):
    """
    Copy file to destination, returns true/false.

    :param str source: string - file to copy.
    :param str destination: string - destination file
    :returns: True if successed
    :rtype: bool

    Example::

        success = xbmcvfs.copy(source, destination)
    """
    try:
        shutil.copyfile(safe_path(source), safe_path(destination))
    except shutil.Error:
        return False
    else:
        return True


# noinspection PyShadowingBuiltins, PyPep8Naming
def deleteFile(file):
    """
    Delete the file

    :param str file: string - file to delete
    :returns: True if successed
    :rtype: bool

    Example::

        success = xbmcvfs.deleteFile(file)
    """
    try:
        os.remove(safe_path(file))
    except EnvironmentError:
        return False
    else:
        return True


def exists(path):
    """
    Check for a file or folder existence

    :param str path: string - file or folder
    :returns: True if successed
    :rtype: bool

    Example::

        success = xbmcvfs.exists(path)
    """
    return os.path.exists(safe_path(path))


def listdir(path):
    """
    Lists content of a folder.

    :param str path: Folder to get list from
    :returns: Directory content list
    :rtype: tuple

    example::

        dirs, files = xbmcvfs.listdir(path)
    """
    dirs = []
    files = []
    path = safe_path(path)
    for item_name in os.listdir(path):
        item_path = os.path.join(path, item_name)
        if os.path.isfile(item_path):
            files.append(item_name)
        else:
            dirs.append(item_name)

    # Return a tuple of (dir, files)
    return dirs, files


def mkdir(path):
    """
    Create a folder.

    :param str path: Folder to create
    :returns: True if successed
    :rtype: bool

    Example::

        success = xbmcvfs.mkdir(path)
    """
    try:
        os.mkdir(safe_path(path))
    except EnvironmentError:
        return False
    else:
        return True


def mkdirs(path):
    """
    Make all directories along the path

    Create folder(s) - it will create all folders in the path.

    :param str path: olders to create.
    :returns: True if successed
    :rtype: bool

    example::

        success = xbmcvfs.mkdirs(path)
    """
    try:
        os.makedirs(safe_path(path))
    except EnvironmentError:
        return False
    else:
        return True


# noinspection PyShadowingBuiltins, PyPep8Naming
def rename(file, newFile):
    """
    Rename a file

    :param str file: string - File to rename
    :param str newFile: string - New filename, including the full path
    :returns: True if successed
    :rtype: bool

    .. note:: Moving files between different filesystem (eg. local to nfs://) is not possible on all platforms.
              You may have to do it manually by using the copy and deleteFile functions.

    Example::

        success = xbmcvfs.rename(file,newFileName)
    """
    try:
        os.rename(safe_path(file), safe_path(newFile))
    except EnvironmentError:
        return False
    else:
        return True


def rmdir(path):
    """
    Remove a folder.

    :param str path: Folder to remove
    :returns: True if successed
    :rtype: bool

    Example::

        success = xbmcvfs.rmdir(path)
    """
    try:
        os.rmdir(safe_path(path))
    except EnvironmentError:
        return False
    else:
        return True


# noinspection PyUnusedLocal, PyMethodMayBeStatic, PyShadowingBuiltins, PyPep8Naming
class File(object):
    """
    File(filepath, mode=None)

    Creates a file object

    :param str filepath: Selected file path
    :param str mode: [opt] string Additional mode options (if no mode is supplied, the default is Open for Read).

    Example::

        f = xbmcvfs.File(file, 'w')
    """

    def __init__(self, filepath, mode=None):
        self._filepath = safe_path(filepath)
        self._file = open(self._filepath, mode if mode else "r")

    def close(self):
        """
        Close the file

        example::

            f = xbmcvfs.File(file)
            f.close()
        """
        self._file.close()

    def read(self, numBytes=0):
        """
        Read from the file to a string.

        :param int numBytes: [opt] How many bytes to read - if not set it will read the whole file
        :returns: data as a string
        :rtype: str

        example::

            f = xbmcvfs.File(file)
            b = f.read()
            f.close()
        """
        return self._file.read()

    def readBytes(self, numBytes=0):
        """
        Read bytes from file.

        :param int numBytes: [opt] How many bytes to read - if not set it will read the whole file
        :return: data as a bytearray
        :rtype: bytearray

        example::

            f = xbmcvfs.File(file)
            b = f.read()
            f.close()
        """
        return bytearray(self.read(numBytes))

    def seek(self, seekBytes, iWhence):
        """
        Seek to position in file.

        :param int seekBytes: position in the file
        :param int iWhence: where in a file to seek from[0 beginning, 1 current , 2 end position]

        example::

            f = xbmcvfs.File(file)
            result = f.seek(8129, 0)
            f.close()
        """
        self._file.seek(seekBytes, iWhence)

    def size(self):
        """
        Get the file size.

        :returns: The file size
        :rtype: long

        example::

            f = xbmcvfs.File(file)
            s = f.size()
            f.close()
        """
        return os.stat(self._filepath).st_size

    def write(self, buffer):
        """
        To write given data in file.

        :param str buffer: Buffer to write to file
        :returns: True on success.
        :rtype: bool

        example::

            f = xbmcvfs.File(file, 'w')
            result = f.write(buffer)
            f.close()
        """
        try:
            self._file.write(buffer)
        except EnvironmentError:
            return False
        else:
            return True


class Stat(object):
    """
    These class return information about a file.
    Execute (search) permission is required on all of the directories in path that lead to the file.

    :param str path: file or folder

    example::

        st = xbmcvfs.Stat(path)
        modified = st.st_mtime()
    """

    def __init__(self, path):
        self._stat = os.stat(safe_path(path))

    def st_atime(self):
        """
        To get time of last access.

        :return: st_atime
        :rtype: long
        """
        return self._stat.st_atime

    def st_ctime(self):
        """
        To get time of last status change.

        :return: st_ctime
        :rtype: long
        """
        return self._stat.st_ctime

    def st_mtime(self):
        """
        To get time of last modification.

        :return: st_mtime
        :rtype: long
        """
        return self._stat.st_mtime

    def st_dev(self):
        """
        To get ID of device containing file.

        The st_dev field describes the device on which this file resides.

        :return: st_dev
        :rtype: long
        """
        return self._stat.st_dev

    def st_gid(self):
        """
        To get group ID of owner.

        :return: st_gid
        :rtype: long
        """
        return self._stat.st_gid

    def st_ino(self):
        """
        To get inode number.

        :return: st_ino
        :rtype: long
        """
        return self._stat.st_ino

    def st_mode(self):
        """
        To get file protection.

        :return: st_mode
        :rtype: long
        """
        return self._stat.st_mode

    def st_nlink(self):
        """
        To get number of hard links.

        :return: st_nlink
        :rtype: long
        """
        return self._stat.st_nlink

    def st_size(self):
        """
        To get total size, in bytes.

        The st_size field gives the size of the file (if it is a regular file or a symbolic link) in bytes.
        The size of a symbolic link (only on Linux and Mac OS X) is the length of the pathname it contains,
        without a terminating null byte.

        :return: st_size
        :rtype: long
        """
        return self._stat.st_size

    def st_uid(self):
        """
        To get user ID of owner.

        :return: st_uid
        :rtype: long
        """
        return self._stat.st_uid


# noinspection PyPep8Naming
def translatePath(path):
    """
    Returns the translated path.

    :param path: string or unicode - Path to format
    :type path: str or unicode

    :returns: Translated path
    :rtype: str

    .. note: Only useful if you are coding for both Linux and Windows.

    Converts ``'special://masterprofile/script_data'`` -> ``'/home/user/XBMC/UserData/script_data'`` on Linux.

    List of Special protocols - http://kodi.wiki/view/Special_protocol

    Example::

        fpath = xbmc.translatePath('special://masterprofile/script_data')
    """
    path = ensure_native_str(path)
    # Return the path unmodified if not a special path
    if not path.startswith("special://"):
        return path

    # Extract the directory name
    special_path, path = path.split("/", 3)[2:]

    # Fetch realpath from the path mapper
    realpath = kodi_paths.get(special_path)
    if realpath is None:
        raise ValueError("%s is not a valid root dir." % special_path)
    else:
        return os.path.join(realpath, *path.split("/"))
