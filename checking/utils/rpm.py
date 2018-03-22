import subprocess


class Rpm(object):
    """ Helper for rpm commands"""
    # TODO: find rpm python bindings that work on RHEL, Centos and Fedora

    @classmethod
    def verify(cls, name, prefix='/host'):
        """Verify files against rpm database, these attributes:
           - Owner
           - Group
           - Mode
           - MD5 Checksum
           - Size
           - Major Number
           - Minor Number
           - Symbolic Link String
           - Modification Time
        """

        try:
            subprocess.check_output(
                ['rpm', '--verify', '--root', prefix, name], close_fds=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
