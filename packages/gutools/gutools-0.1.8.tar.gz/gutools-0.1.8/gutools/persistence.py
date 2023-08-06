
"""This module provide a Persiste using sqlite
"""

import sqlite3
import time
from datetime import datetime
import os
import random
import threading
import hashlib
import yaml
import re
import ujson as json
from collections import namedtuple, defaultdict
from typing import Iterable
from weakref import WeakKeyDictionary

from aiopb.aiopb import Hub
from gutools.tools import uidfrom, snake_case, expandpath, retry, identity, \
    yaml_encode, yaml_decode, test_pid, walk, rebuild, serializable_container
from gutools.uobjects import UObject

class FileLock(object):
    """Open a file with exclusive access.
    FileLock is used as a context manager returning the file stream opened
    with the desired access mode ('w', 'r', 'a').

    When a program wants to update a file in the session,
    FileLock can be used to prevent only one file will get the access.

    FileLock proceed as follows:

    - check for ``<filename>.lock``
    - if does not exist, or the modification timestamp is older, then
      it will create the file with the content: ``<pid>.<threadid>.<random>``
    - then check again the file.
    - read the file and check that the content is the same.
    - then acquire the lock.
    - update file.
    - remove the lock file.

    In case two processes try to access at the same time, the file creation
    is an atomic operation, so only one process will read its own content.
    """
    def __init__(self, path, mode='w', timeout=0):
        """
        - ``path``: the file to get access to.
        - ``mode``: the desired access mode.
        - ``timeout``: for getting the lock.
        """
        self.path = path
        self.lock_file = path + '.lock'
        self.mode = mode
        self.timeout = timeout
        self.fd = None
        self.lock_fd = None

    def __enter__(self):
        """Try to write a specific content (like a fingerprint)
        in a lock file, and check if the content is the same afterall.
        If content match, then the access is granted and return the
        real file opened in the given access mode.
        """
        content = f'{os.getpid()}.{threading.current_thread().name}.{random.random()}'

        def test():
            try:
                return open(self.lock_file, 'r').read()
            except OSError:
                return ''

        now = time.time()
        pid = os.getpid()
        while self.timeout and time.time() - now < self.timeout:
            content2 = test()
            if content == content2:
                break
            if not content2 or not test_pid(content2.split('.')[0]):
                open(self.lock_file, 'w').write(content)
                continue
            time.sleep(random.random() / 10.0)
        else:
            raise TimeoutError(f"Locking {self.path} for {self.mode}")

        self.fd = open(self.path, self.mode)
        return self.fd

    def __exit__(self, *args):
        """Remove the lock and close the file."""
        os.unlink(self.lock_file)
        self.fd.close()
        self.fd = None


class FSLayout(object):
    """Handle files contents based on predeterminated patterns and structure.
    """
    reg_file_params = re.compile(
        r'(?P<workspace>.*)/(?P<key>[^/]+)/(?P<name>\w+-\w+)(\.(?P<label>.*))?\.(\2)',
        re.DOTALL)

    ext_decoder = {
        'yaml': yaml_decode,
        'json': json.decode,
        'pid': int,
        'out': identity,
        'err': identity,
    }

    ext_encoder = {
        'yaml': yaml_encode,
        'json': json.encode,
        'pid': str,
        'out': identity,
        'err': identity,
    }

    ext_aliases = {
        'fp': 'yaml',
    }

    for k, v in ext_aliases.items():
        ext_decoder[k] = ext_decoder[v]
        ext_encoder[k] = ext_encoder[v]

    patterns = {
        ('out', 'err', 'pid', 'fp', 'db'): '{root:}/{key:}/{name:}.{key:}',
        ('etc', ): '{root:}/etc/{name:}.yaml',
        ('<folder>', ) : '{root:}/{name:}'
    }

    def __init__(self, path):
        self.path = expandpath(path)
        self.stat = dict()
        """Dictionary with last modification of a file.
        Is updated by ``get/set_content()``"""

    def get_path(self, key, *args, touch=False):
        """Get a the file (or folder) of the key expanded with given args.

        When ``touch=True`` the file is *touched* and create all necessary
        parent folders.
        """
        path = ''
        root = self.path
        name = '.'.join(['{}'] * len(args)).format(*args)
        for pattern, fmt in self.patterns.items():
            if key in pattern:
                path = fmt.format(**locals())
                break
        else:
            raise RuntimeError(f"Key '{key}' found to expand path")

        assert path
        if touch:
            if key in ('<folder>', ):
                os.makedirs(path, exist_ok=True)
            else:
                parent = os.path.dirname(path)
                os.makedirs(parent, exist_ok=True)
        return path

    def get_content(self, key, *args, default=None):
        """Get the content of a file in the layout structure,
        setting with default when file does not exists."""
        path = self.get_path(key, *args)
        content = self._get_content(path)
        if content is None and default is not None:
            content = default
            self.set_content(key, content, *args)
        try:
            self.stat[path] = [os.stat(path).st_mtime, (key, args)]
        except FileNotFoundError:
            pass
        return content

    def set_content(self, key, content, *args):
        """Set the content of a key/args in the layout structure.
        Uses a FileLock to have exclusive access to file.
        """
        path = self.get_path(key, *args)
        parent = os.path.dirname(path)
        os.makedirs(parent, exist_ok=True)
        content = serializable_container(content)

        with FileLock(path, timeout=3) as f:
            try:
                func = self.ext_encoder.get(path.split('.')[-1], identity)
                f.write(func(content))
                self.stat[path] = [os.stat(path).st_mtime, (key, args)]

            except Exception as why:
                path = None
        return path

    def update_content(self, key, content, *args):
        """Update the content of a key/args in the layout structure.

        - read the current content
        - update the content
        - save the file
        - return content last state
        """
        content2 = self.get_content(key, *args, default=content)
        content2.update(content)
        self.set_content(key, content, *args)
        return content2

    def iter_file_content(self, key, name='', label='', *args):
        """Iterate over known files handled by the layout structure
        filtering name and label if they are provided.
        """
        dummy = self.get_path(key, '__dummy__')
        top = os.path.dirname(dummy)
        for root, _, files in os.walk(top):
            for name_ in files:
                filename = os.path.join(root, name_)
                m = self.reg_file_params.search(filename)
                if m:
                    d = m.groupdict()
                    if name in ('', d['name']) and \
                       label in ('', d['label']):
                        content = self._get_content(filename)
                        if content is not None:
                            yield d, filename, content

    def iter_external_modifications(self):
        """Iterator for external known file modifications."""
        for path, (mtime, params) in list(self.stat.items()):
            try:
                mtime2 = os.stat(path)
                if mtime2 > mtime:
                    yield path, params
            except OSError:
                self.stat.pop(path)

    def set_alias(self, key, alias, *args):
        """Set an alias of a file by creating a symbolic
        link between files.
        """
        src, dst = self._alias_info(key, alias, *args)
        if src != dst:
            assert os.path.exists(src)
            if os.path.exists(dst):
                os.remove(dst)
            # cd dir to make link relative and less anoying when `ls -ls`
            # don't work!
            # curdir = expandpath(os.path.curdir)
            # os.chdir(os.path.dirname(dst))
            # os.symlink(src, os.path.basename(dst))
            # os.chdir(curdir)
            os.symlink(src, dst)
            assert os.path.islink(dst)

    def remove_alias(self, key, alias, *args):
        """Remove an alias of a file."""
        src, dst = self._alias_info(key, alias, *args)
        assert os.path.islink(dst)
        os.remove(dst)

    def _alias_info(self, key, alias, *args):
        "compute the source and target for an alias."
        src = self.get_path(key, *args)
        dst, ext = os.path.splitext(src)
        dst = list(os.path.split(dst))
        dst[-1] = alias + ext
        dst = os.path.join(*dst)
        return src, dst

    def _get_content(self, filename, default=None):
        "get the content of a file, retuning default value if does not exists."
        try:
            with open(filename) as f:
                content = f.read()
                func = self.ext_decoder.get(filename.split('.')[-1], identity)
                content = func(content)
        except FileNotFoundError as why:
            content = default
        return content

# --------------------------------------------------
# Configurable
# --------------------------------------------------
class Config(dict):
    def __init__(self, layout, name, default={}):
        self.layout = layout
        self.name = name
        if default:
            self.update(default)

    def load(self, default={}):
        self.clear()
        data = self.layout.get_content(
            'etc', self.name,
            default=default)
        self.update(data)


    def save(self, name=None):
        name = name or self.name
        self.config = self.layout.set_content(
            'etc', self, self.name)

    def update_key(self, key, values):
        v0 = self.get(key)
        if isinstance(v0, dict) and isinstance(values, dict):
            v0.update(values)
        elif isinstance(v0, list) and isinstance(values, Iterable):
            v0 = set(v0)
            v0.update(values)
            self[key] = list(v0)
        else:
            self[key] = values

        self.save()


class DB(object): # , metaclass=Xingleton):
    """This class provide a Persiste Logging events using sqlite.

    As sqlite doesn't suppor shared connection between threads,
    we implement a simple connection factory for the current thread.
    """
    scheme = ""

    def __init__(self, path=None, delete=False):
        self.path = expandpath(path)
        self.conn__ = dict()
        self.workspaces = WeakKeyDictionary()

        if delete and os.path.exists(self.path):
            os.unlink(self.path)

    def __del__(self):
        self.conn.commit()

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.conn.commit()

    def __str__(self):
        return f"<{self.__class__.__name__}: {self.path}>"

    def __repr__(self):
        return str(self)

    @property
    def conn(self):
        "Connection Factory per thread"
        tid = threading.get_ident()

        conn = self.conn__.get(tid)
        if conn is None:
            self.conn__[tid] = conn = sqlite3.connect(self.path)
        return conn

    def close(self):
        """Clear the processed event and close connections with database"""
        for conn in list(self.conn__.values()):
            try:
                conn.commit()
                conn.close()
            except sqlite3.ProgrammingError:
                pass

    # def get(self, since=0):
        # cursor = self.conn.cursor()
        # cursor.execute(SELECT, (since, ))
        # for raw in cursor.fetchall():
            # if raw:
                # event = Event(*raw)
                # yield event

    def execute(self, query, *args, **kw):
        conn = self.conn
        if args:
            r = conn.execute(query, args)
        else:
            r = conn.execute(query, kw)
        return r

    def executescript(self, script):
        conn = self.conn
        try:
            conn.executescript(script)
        except sqlite3.OperationalError as why:
            print('FAILED TO CREATE DB SCHEME: {}'.format(why))
            print(script)
            foo = 1
        conn.commit()

    # workspace management
    @property
    def ready(self):
        return self.path is not None

    def attach(self, workspace):
        self.workspaces[workspace] = True #  keep a life reference
        if self.ready:
            workspace.db_ready()

    def change_db(self, path):
        self.path = path
        # force new operations to create a new sqlite3 connection per thread
        self.conn__.clear()
        for workpace in self.workspaces:
            workpace.db_ready()


class DBWorkspace(object):
    scheme = ""
    REPLACE = 'REPLACE INTO {table:} ({})  VALUES (:{})'
    INSERT = 'INSERT INTO {table:} ({})  VALUES (:{})'
    SELECT = 'SELECT * FROM {table:} WHERE {where:}'
    DELETE = 'DELETE FROM {table:} WHERE {}'

    uobject_table = dict()

    def __init__(self, db):
        self.db = db
        self.db.attach(self)

    def db_ready(self):
        if self.db.ready:
            self.__create_squema__()

    def __create_squema__(self):
        try:
            self.db.executescript(self.scheme)
            self.db.conn.commit()
        except Exception as why:
            print(why)
            retry(1)

    @classmethod
    def _get_table(cls, klass):
        table = cls.uobject_table.get(klass)
        if table is None:
            table = snake_case(klass.__name__)
            cls.uobject_table[klass] = table
        return table

    def update(self, uobject, sql=None, table=None, **kwargs):
        table = table or self._get_table(uobject.__class__)
        sql = sql or self.REPLACE

        kw = uobject.asdict(skip_nones=True, **kwargs)
        # for k in set(uobject.__slots__).intersection(kwargs):
            # kw[k] = kwargs[k]

        if 'date' in kw and kw.get('date') is None:
            kw['date'] = datetime.now()

        sql = sql.format(','.join(kw.keys()),
                                      ',:'.join(kw.keys()),
                                      table=table, )
        self.db.execute(sql, **kw)
        for tries in range(20):
            try:
                self.db.conn.commit()
                break
            except sqlite3.OperationalError:
                time.sleep(random.random())

    def xupdate(self, uobject, **kw):
        self.update(uobject, **kw)
        kw.update(uobject.asdict())
        for full_object in self.find(uobject.__class__, **kw):
            return full_object

    def replace(self, uobject, **kw):
        kw.update(uobject.asdict())
        for full_object in self.find(uobject.__class__, **kw):
            break
        else:
            return self.xupdate(uobject, **kw)

    def delete_item(self, uobject):
        table = self._get_table(uobject.__class__)
        kw = uobject.asdict(skip_nones=True)
        sql = self.DELETE.format(' AND '.join([f'{k}=:{k}' for k in kw.keys()]),
                                 table=table, )
        self.db.execute(sql, **kw)
        self.db.conn.commit()

    def delete(self, klass, join='AND', sql=None, table=None, **kw):
        table = table or self._get_table(klass)
        sql = sql or self.DELETE

        for row in self._execute(klass, sql, join=join, table=table, **kw):
            item = klass(*row)
            yield item

    def find(self, klass, join='AND', sql=None, table=None, **kw):
        table = table or self._get_table(klass)
        sql = sql or self.SELECT

        for row in self._execute(klass, sql, join=join, table=table, **kw):
            item = klass(*row)
            yield item

    def _execute(self, klass, sql, join='AND', **kw):
        where = [k for k in set(kw).intersection(
            klass.__slots__) if kw[k] is not None]

        where = f' {join} '.join([f'{k}=:{k}' for k in where]) or '1'

        sql = sql.format(where=where, **kw)
        iterator = self.db.execute(sql, **kw)
        return iterator

def test_file_locking():
    layout = FSLayout(path='/tmp/kk')
    content = dict(foo=1, bar='dos')
    path = layout.set_content('etc', content, 'buzz')

    with FileLock(path, mode='a', timeout=100) as f1:
        with FileLock(path, mode='a', timeout=2) as f2:
            foo = 1
    foo = 1


if __name__ == '__main__':
    test_file_locking()
