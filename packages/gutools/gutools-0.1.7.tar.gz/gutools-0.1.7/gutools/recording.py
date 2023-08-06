import lzma
import gzip
import bz2
from datetime import datetime


class Recorder(object):
    """Support events recording for rotating compressed files.
    
    By default lzma compression is selected (a.k.a. 'xz' files)
    
    The default time_fmt used as timestamp is '%Y-%m-%d %H:%M:%S.%f'
    allowing microseconds precission
    
    The default grouping criteria is records that share the same day.
    This is made by rotate_by = '%Y%m%d', so all records that share the
    same day when are saved belongs to the same record file.
    
    If you want to record some keys in the same file just use ``aliases``
    parameter to convert keys before duming record.
    
    """
    INFO = {
        'xz': lzma,
        'gz': gzip,
        'bz2': bz2,
    }
    
    
    def __init__(self, compression='xz',
                 time_fmt='%Y-%m-%d %H:%M:%S.%f',
                 rotate_by='%Y%m%d',
                 aliases=None, *args, **kw):
        self.compression = compression
        self.time_fmt = time_fmt
        self.rotate_by = rotate_by
        self.aliases = aliases or dict()
        
        self._output = dict()
        self._last_flush = dict()

    def record(self, key, *event):
        # write market data file
        t = datetime.utcnow()
        now = t.strftime(self.time_fmt)
        today = t.strftime(self.rotate_by)
        outputs = self._output.get(key)
        if not outputs:
            outputs = self._output[key] = dict()

        output = outputs.get(today)
        if not output:
            # rotate dump file
            for k in list(outputs.keys()):
                output.pop(k).close()

            # set the new one
            output = outputs[today] = self.INFO[self.compression].\
                open(f"{key}.{today}.{self.compression}", 'a')

        line = [str(k) for k in event]
        line = '.'.join(line) + '\n'
        output.write(bytes(line, 'utf-8'))

        last_flush = self._last_flush.setdefault(key, t)
        if (t - last_flush).seconds > 120:
            output._fp.flush()
            output.close()  # will be reopen next write attempt
            outputs.pop(today)
            self._last_flush[key] = t

    def close(self):
        for _, keys in self._output.items():
            for k, f in keys.items():
                print(f"Closing dump file: {f._fp.name}")
                f._fp.flush()
                f.close()

