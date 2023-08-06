# Author: Toshio Kuratomi <tkuratom@redhat.com>
# License: GPLv3+
# Copyright: Ansible Project, 2020
"""Parse documentation from ansible plugins using ansible apis."""

# TODO:
# We're going to need to replace ansible-doc parsing with our own parser.
# Use pkgutil.walk_packages() and pkgutil.iter_modules() to do that.
# From nitzmahone:
# the only problem with walk_packages is that you can't stop it, so it's incredibly wasteful at
# the root (but does work since the routing PR merged). So if you use iter_modules manually on the
# first couple levels to locate the collections themselves, then you can use walk_packages on the
# subpackages to locate the plugins themselves, and/or this thing I've been toying with for generic
# resource enumeration


def plugin_output_directory(plugin_type, output_dir):
    """
    Determine the output directory based on the plugin_type

    For backwards link compatibility, modules are in a toplevel modules directory while other
    plugins are in a subdirectory of plugins
    """
    if plugin_type in ('module', 'module_util'):
        return '%s/%ss' % (output_dir, plugin_type)
    return '%s/plugins/%s' % (output_dir, plugin_type)


def plugin_filename_format(plugin_type):
    """
    Determine the filename format string to use for this type of plugin

    For backwards link compatibility, modules use a format of ``<module>_module.rst``
    whereas other plugins just use ``<module>.rst``.
    """
    if plugin_type == 'module':
        output_name = '%s_' + '%s.rst' % plugin_type
    else:
        # for plugins, just use 'ssh.rst' vs 'ssh_module.rst'
        output_name = '%s.rst'

    return output_name
