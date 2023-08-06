# -*- coding: utf-8 -*-
"""
    sphinxcontrib.ditaa
    ~~~~~~~~~~~~~~~~~~~~~

    Allow ditaa commands be rendered as nice looking images
    

    See the README file for details.

    :author: Vadim Gubergrits <vadim.gubergrits@gmail.com>
    :license: BSD, see LICENSE for details

    Inspired by ``sphinxcontrib-aafig`` by Leandro Lucarella.
"""

import re, os
import codecs
import posixpath
from os import path
from math import ceil
from subprocess import Popen, PIPE
try:
    from hashlib import sha1 as sha
except ImportError:
    from sha import sha

from docutils import nodes
from docutils.parsers.rst import directives

from sphinx.errors import SphinxError
from sphinx.util import ensuredir, relative_uri
#from sphinx.util.compat import Directive

def get_hashid(text,options):
    hashkey = text.encode('utf-8') + str(options).encode('utf-8')
    hashid = sha(hashkey).hexdigest()
    return hashid


class DitaaError(SphinxError):
    category = 'ditaa error'


class DitaaDirective(directives.images.Image):
    """
    Directive that builds plots using ditaa.
    """
    has_content = True
    required_arguments = 0
    own_option_spec = dict( {
        '--no-antialias': str,
        '--background': str,
        '--no-separation': str,
        '--encoding': str,
        '--html': str,
        '--overwrite': str,
        '--round-corners': str,
        '--no-shadows': str,
        '--scale': str,
        '--transparent': str,
        '--tabs': str,
        '--fixed-slope': str,
        }

    )

    option_spec = directives.images.Image.option_spec.copy()
    option_spec.update(own_option_spec)
    #print(option_spec)
  
    def run(self):
        self.arguments = ['']
        #print("self.options: %s" %(self.options))
        ditaa_options = dict([(k,v) for k,v in self.options.items() 
                                  if k in self.own_option_spec])

        (image_node,) = directives.images.Image.run(self)
        if isinstance(image_node, nodes.system_message):
            return [image_node]
        text = '\n'.join(self.content)
        image_node.ditaa = dict(text=text,options=ditaa_options)
        return [image_node]


def render_ditaa_images(app, doctree):
    #print("app.builder.env.docname: %s" %(app.builder.env.docname))
    #print("app.builder.format: %s" %(app.builder.format))
    #print(nodes)
    #print(dir(nodes))
    for img in doctree.traverse(nodes.image):
        if not hasattr(img, 'ditaa'):
            continue

        text = img.ditaa['text']
        options = img.ditaa['options']
        try:
            relfn, outfn = render_ditaa(app, text, options, app.builder.format, "ditaa")
            img['uri'] = relfn
        except DitaaError:
            #app.builder.warn('ditaa error: ')
            img.replace_self(nodes.literal_block(text, text))
            continue

def render_ditaa(app, code, options, format, prefix='ditaa'):
    """Render ditaa code into a PNG output file."""
    hashkey = code + str(options) + \
              str(app.builder.config.ditaa) + \
              str(app.builder.config.ditaa_args)
    hashkey = hashkey.encode('utf-8')
    infname = '%s-%s.%s' % (prefix, sha(hashkey).hexdigest(), "ditaa")
    outfname = '%s-%s.%s' % (prefix, sha(hashkey).hexdigest(), app.builder.config.ditaa_output_suffix)

    #rel_imgpath = (format == "html") and relative_uri(app.builder.env.docname, app.builder.imagedir) or ''
    if format == 'html':
        rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    elif format == 'latex':
        rel_imgpath = relative_uri(app.builder.env.docname, app.builder.imagedir)
    else:
        app.builder.warn('gnuplot: the builder format %s is not officially supported.' % format)

    infullfn = path.join(app.builder.outdir, app.builder.imagedir, infname)
    outrelfn = posixpath.join(rel_imgpath, outfname)
    outfullfn = path.join(app.builder.outdir, app.builder.imagedir, outfname)
    #inrelfn = posixpath.join(relative_uri(app.builder.env.docname, app.builder.imagedir), infname)

    if path.isfile(outfullfn):
        return outrelfn, outfullfn

    ensuredir(path.dirname(outfullfn))
    # ditaa expects UTF-8 by default
    #if isinstance(code, unicode): code = code.encode('utf-8')
    code = code.encode('utf-8')

    ditaa_args = [app.builder.config.ditaa]
    ditaa_args.extend(app.builder.config.ditaa_args)
    #print(options)
    for item in options.keys():
        ditaa_args.append(item)  
        if options[item] != "None":
            ditaa_args.append(options[item])  
        #ditaa_args.append(options)
    ditaa_args.extend( [infname, outfname] ) # use relative path
    f = open(infullfn, 'wb')
    f.write(code)
    f.close() 
    currpath = os.getcwd()
    os.chdir(path.join(app.builder.outdir, app.builder.imagedir))

    try:
        if app.builder.config.ditaa_log_enable:
            print("rending %s in %s.rst" %(outfullfn, app.builder.env.docname))
        #app.builder.warn(ditaa_args)
        #print(ditaa_args)
        p = Popen(ditaa_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    except OSError as err:
        if err.errno != ENOENT:   # No such file or directory
            raise DitaaError("error")
        app.builder.warn('ditaa command %r cannot be run (needed for ditaa '
                          'output), check the ditaa setting' %
                          app.builder.config.ditaa)
        app.builder._ditaa_warned_dot = True
        os.chdir(currpath)
        return None, None

    os.chdir(currpath)
    wentWrong = False
    try:
        # Ditaa may close standard input when an error occurs,
        # resulting in a broken pipe on communicate()
        stdout, stderr = p.communicate(code)
        #print(stdout.decode("utf-8"))
    except OSError as err:
        if err.errno != EPIPE:
            raise DitaaError("error")
        wentWrong = True
    except IOError as err:
        if err.errno != EINVAL:
            raise DitaaError("error")
        wentWrong = True
    if wentWrong:
        # in this case, read the standard output and standard error streams
        # directly, to get the error message(s)
        stdout, stderr = p.stdout.read(), p.stderr.read()
        p.wait()
    if p.returncode != 0:
        raise DitaaError('ditaa exited with error:\n[stderr]\n%s\n'
                            '[stdout]\n%s' % (stderr, stdout))
    return outrelfn, outfullfn

def setup(app):
    app.add_directive('ditaa', DitaaDirective)
    app.connect('doctree-read', render_ditaa_images)
    app.add_config_value('ditaa', 'ditaa', 'html')
    app.add_config_value('ditaa_args', [], 'html')
    app.add_config_value('ditaa_output_suffix', 'png', 'html')
    app.add_config_value('ditaa_log_enable', True, 'html')
