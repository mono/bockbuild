import re
import glob
import os
import sys
import subprocess
import fileinput
import inspect
import time
import difflib


def log(phase, message):
    # DISABLED until we can properly refactor/redirect logging
    return


def warn(message):
    print '(bockbuild warning) %s' % message


def error(message):
    print '(bockbuild error) %s' % message
    sys.exit(255)


def retry(func, tries=3, delay=5):
    result = None
    exc = None
    for x in range(tries):
        try:
            result = func()
            return result
        except Exception as e:
            if x == tries - 1:
                raise
            warn(str(e))
            warn("Retrying ''%s'' in %s secs" % (func.__name__, delay))
            time.sleep(delay)


def update(new_text, file):
    if not os.path.exists(file):
        open(file, 'w+').close()
    orig_text = open(file).readlines()
    difflines = [
        line for line in difflib.context_diff(orig_text, new_text, n=0)]
    if len(difflines) > 0:
        output = open(file, 'w')
        output.writelines(new_text)
        # for line in new_text:
        #	output.write (line + '\n')
        return difflines
    else:
        return None


def dump(self, name):
    for k in self.__dict__.keys():
        if isinstance(self.__dict__[k], (str, list, tuple, dict, bool, int)) and not k.startswith('_'):
            yield '%s.%s = "%s"\n' % (name, k, self.__dict__[k])


def expand_macros(node, vars, extra_vars=None):
    def sub_macro(m):
        type = m.groups()[0]
        expr = m.groups()[1]
        if type == '%':
            expr = 'self.' + expr

        resolved = False
        for var in [vars, extra_vars]:
            try:
                o = eval(expr, {}, {'self': var})
                resolved = True
                break
            except:
                pass
        if not resolved:
            error("'%s' could not be resolved in string '%s'" %
                  (m.groups()[1], node))
        if o == None:
            return ''
        elif isinstance(o, (list, tuple)):
            return ' '.join(o)
        return str(o)

    if hasattr(node, '__dict__'):
        for k, v in node.__dict__.iteritems():
            if not k.startswith('_'):
                node.__dict__[k] = expand_macros(v, vars)
    elif isinstance(node, dict):
        for k, v in node.iteritems():
            node[k] = expand_macros(v, vars)
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            node[i] = expand_macros(v, vars)
    elif isinstance(node, str):
        orig_node = node
        iters = 0
        while True:
            v = re.sub('(?<!\\\)([%$]){([^}]+)}',
                       sub_macro, node)
            if v == node:
                break
            iters += 1
            if iters >= 500:
                sys.exit('Too many macro substitutions, possible recursion:'
                         '\'%s\'' % orig_node)
            node = v

    return node


def replace_in_file(filename, word_dic):
    rc = re.compile('|'.join(map(re.escape, word_dic)))

    def translate(match):
        return word_dic[match.group(0)]
    for line in fileinput.FileInput(filename, inplace=1):
        print rc.sub(translate, line)


def run_shell(cmd, print_cmd=False):
    if print_cmd:
        print '++', cmd
    proc = subprocess.Popen(cmd, shell=True)
    exit_code = os.waitpid(proc.pid, 0)[1]
    if not exit_code == 0:
        print
        raise Exception(
            'ERROR: command exited with exit code %s: %s' % (exit_code, cmd))


def backtick(cmd, print_cmd=False):
    if print_cmd:
        print '``', cmd
    lines = []
    for line in os.popen(cmd).readlines():
        lines.append(line.rstrip('\r\n'))
    return lines


def get_host():
    search_paths = ['/usr/share', '/usr/local/share']
    am_config_guess = []
    for path in search_paths:
        am_config_guess.extend(glob.glob(os.path.join(
            path, os.path.join('automake*', 'config.guess'))))
    for config_guess in am_config_guess:
        config_sub = os.path.join(os.path.dirname(config_guess), 'config.sub')
        if os.access(config_guess, os.X_OK) and os.access(config_sub, os.X_OK):
            return backtick('%s %s' % (config_sub, backtick(config_guess)[0]))[0]
    return 'python-%s' % os.name


def get_cpu_count():
    try:
        return os.sysconf('SC_NPROCESSORS_CONF')
    except:
        return 1
