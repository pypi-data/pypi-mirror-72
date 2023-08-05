from ipykernel.kernelbase import Kernel
from pexpect import replwrap, EOF
import pexpect

from subprocess import PIPE, Popen
import signal
import re
import os

__version__ = '0.2.2'

class ACL2Kernel(Kernel):
    implementation = 'acl2_kernel'
    implementation_version = __version__

    @property
    def language_version(self):
        with Popen(os.environ['ACL2'], stdout=PIPE, stdin=PIPE) as p:
            p.stdin.close()
            return re.findall(r'ACL2 Version.*$', p.stdout.read().decode('utf-8'), re.MULTILINE)[0]
    
    @property
    def banner(self):
        return u'ACL2 Kernel (%s)' % self.language_version
    
    language_info = {
        'name': 'acl2',
        'codemirror_mode': 'lisp',
        'mimetype': 'text/x-lisp',
        'file_extension': '.lisp'
    }

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self._start_acl2()

    def _start_acl2(self):
        sig = signal.signal(signal.SIGINT, signal.SIG_DFL)
        try:
            self.acl2wrapper = replwrap.REPLWrapper(os.environ['ACL2'], 'ACL2 !>', None)
        finally:
            signal.signal(signal.SIGINT, sig)
        
    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if not code.strip():
            return {
                'status': 'ok',
                'execution_count': self.execution_count,
                'payload': [],
                'user_expressions': []
            }
        interrupted = False
        try:
            cmd = re.sub(r'[\r\n]|;[^\r\n]*[\r\n]+', ' ', code.strip())
            output = self.acl2wrapper.run_command(cmd, timeout=None)
        except KeyboardInterrupt:
            self.acl2wrapper.child.sendintr()
            interrupted = True
            self.acl2wrapper._expect_prompt()
            output =  self.acl2wrapper.child.before
            self.process_output(output)
        except EOF:
            output = self.acl2wrapper.child.before + 'Restarting ACL2'
            self._start_acl2()
            self.process_output(output)
        if interrupted:
            return {
                'status': 'abort',
                'execution_count': self.execution_count
            }
        if not silent:
            stream_content = {
                'execution_count': self.execution_count,
                'name': 'stdout',
                'text': output
            }
            self.send_response(self.iopub_socket, 'stream', stream_content)
        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {}
        }
