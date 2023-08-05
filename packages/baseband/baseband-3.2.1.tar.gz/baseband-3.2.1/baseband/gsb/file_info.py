# Licensed under the GPLv3 - see LICENSE
from astropy import units as u

from ..vlbi_base.file_info import (VLBIFileReaderInfo, VLBIStreamReaderInfo,
                                   info_item)


def file_size(fh):
    offset = fh.tell()
    try:
        return fh.seek(0, 2)
    finally:
        fh.seek(offset)


class GSBTimeStampInfo(VLBIFileReaderInfo):
    attr_names = ('format', 'mode', 'number_of_frames', 'frame_rate',
                  'start_time', 'readable', 'missing', 'errors', 'warnings')
    _header0_attrs = ('mode',)

    @info_item
    def header0(self):
        with self._parent.temporary_offset(0) as fh:
            return fh.read_timestamp()

    @info_item(needs='header0')
    def format(self):
        return 'gsb'

    @info_item(needs='header0')
    def number_of_frames(self):
        with self._parent.temporary_offset() as fh:
            fh_size = fh.seek(0, 2)
            # Guess based on a fixed header size.  In reality, this
            # may be an overestimate as the headers can grow in size,
            # or an underestimate as the last header may be partial.
            # So, search around to be sure.
            guess = max(fh_size // self.header0.nbytes, 1)
            while self.header0.seek_offset(guess) > fh_size:
                guess -= 1
            while self.header0.seek_offset(guess) < fh_size:
                guess += 1

            # Now see if there is indeed a nice header before.
            fh.seek(self.header0.seek_offset(guess-1))
            line_tuple = fh.readline().split()
            # But realize that sometimes an incomplete header is written.
            if (len(" ".join(line_tuple))
                    < len(" ".join(self.header0.words))):
                self.warnings['number_of_frames'] = (
                    'last header is incomplete and is ignored')
                retry = True
            else:
                # Check last header is readable.
                try:
                    self.header0.__class__(line_tuple).time
                except Exception as exc:
                    self.warnings['number_of_frames'] = (
                        'last header failed to read ({}) and is ignored'
                        .format(str(exc)))
                    retry = True
                else:
                    retry = False
            if retry:
                guess -= 1
                fh.seek(self.header0.seek_offset(guess-1))
                self.header0.fromfile(fh).time

        return guess

    # Cannot know whether it is readable without the raw data files.
    readable = None

    @info_item
    def missing(self):
        missing = super().missing
        missing['raw'] = 'need raw binary files for the stream reader'
        return missing


class GSBStreamReaderInfo(VLBIStreamReaderInfo):
    attr_names = list(VLBIStreamReaderInfo.attr_names)
    attr_names.insert(attr_names.index('readable'), 'bandwidth')
    attr_names.insert(attr_names.index('readable'), 'n_raw')
    attr_names.insert(attr_names.index('readable'), 'payload_nbytes')
    attr_names = tuple(attr_names)

    _parent_attrs = VLBIStreamReaderInfo._parent_attrs + ('payload_nbytes',)

    @info_item
    def frame0(self):
        return self._parent._read_frame(0)

    # Bit of a hack, but the base reader one suffices here with
    # the frame0 override above.
    decodable = VLBIFileReaderInfo.decodable

    @info_item
    def file_info(self):
        fh_ts_info = self._parent.fh_ts.info
        fh_ts_info.missing.pop('raw', None)
        return fh_ts_info

    @info_item(needs='shape')
    def bandwidth(self):
        return (self.sample_rate * self.shape[-1]
                / (1 if self.complex_data else 2)).to(u.MHz)

    @info_item
    def n_raw(self):
        fh_raw = self._parent.fh_raw
        return len(fh_raw[0]) if isinstance(fh_raw, (list, tuple)) else 1

    @info_item(needs=('file_info', 'payload_nbytes', 'n_raw'), default=False)
    def consistent(self):
        pl_nbytes = self.payload_nbytes
        nchan = self._parent._unsliced_shape[-1]
        expected_size = int(((self.stop_time-self.start_time)
                             * self.sample_rate * nchan
                             * self.bps * (2 if self.complex_data else 1)
                             // (8 * self.n_raw)).to(u.one).round())
        fh_raw = self._parent.fh_raw
        if self.file_info.mode == 'rawdump':
            fh_raw = [[fh_raw]]

        msg = ''
        try:
            for pair in fh_raw:
                for fh in pair:
                    fs = file_size(fh)
                    if fs % pl_nbytes != 0 and 'non-integer' not in msg:
                        msg += ('raw file contains non-integer number ({}) '
                                'of payloads.'.format(fs / pl_nbytes))

                    consistent = fs >= expected_size
                    if not consistent:
                        emsg = 'raw file size smaller than expected.'
                        ratio = fs / expected_size
                        if len(pair) == 1 and 0.5 <= ratio < 0.6:
                            emsg = (emsg[:-1] + ' by {} factor of two. '
                                    'Are you missing the second raw file?'
                                    .format('a' if ratio == 0.5
                                            else 'about a'))
                        raise EOFError(emsg)

                    if fs > expected_size and 'more bytes' not in msg:
                        msg += 'raw file contains more bytes than expected.'
        finally:
            if msg:
                self.warnings['consistent'] = msg

        # As a final sanity check, try reading the final sample of the file.
        old_offset = self._parent.tell()
        try:
            self._parent.seek(-1, 2)
            self._parent.read(1)
        finally:
            self._parent.seek(old_offset)

        return True

    @info_item(needs='frame0', default=False)
    def readable(self):
        """Whether the file is readable and decodable."""
        self.checks['decodable'] = self.decodable
        self.checks['consistent'] = self.consistent
        return all(bool(v) for v in self.checks.values())
