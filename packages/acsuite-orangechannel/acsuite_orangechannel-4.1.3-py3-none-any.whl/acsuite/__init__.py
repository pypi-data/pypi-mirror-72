"""Frame-based cutting/trimming/splicing of audio with VapourSynth."""
__all__ = ['eztrim']
__author__ = 'Dave <orangechannel@pm.me>'
__date__ = '29 June 2020'
__credits__ = """AzraelNewtype, for the original audiocutter.py.
Ricardo Constantino (wiiaboo), for vfr.py from which this was inspired.
"""

import os
from pathlib import Path
from re import compile, IGNORECASE
from shutil import which
from subprocess import PIPE, run
from typing import cast, Dict, List, Optional, Tuple, Union
from warnings import simplefilter, warn

import vapoursynth as vs

simplefilter("always")  # display warnings


def eztrim(clip: vs.VideoNode,
           /,
           trims: Union[List[Tuple[int, int]], Tuple[int, int]],
           audio_file: Union[Path, str],
           outfile: Optional[Union[Path, str]] = None,
           *,
           mkvmerge_path: Optional[Union[Path, str]] = None,
           ffmpeg_path: Optional[Union[Path, str]] = None,
           quiet: bool = False,
           debug: bool = False
           ) -> Optional[Dict[str, Union[int, List[int], List[str]]]]:
    """
    Simple trimming function that follows VapourSynth/Python slicing syntax.

    End frame is NOT inclusive.

    For a 100 frame long VapourSynth clip (``src[:100]``):

    ``src[3:22]+src[23:40]+src[48]+src[50:-20]+src[-10:-5]+src[97:]`` can be (almost) directly entered as
    ``trims=[(3,22),(23,40),(48,49),(50,-20),(-10,-5),(97,0)]``.

    ``src[3:-13]`` can be directly entered as ``trims=(3,-13)``.

    :param clip:          Input clip needed to determine framerate for audio timecodes
                          and ``clip.num_frames`` for negative indexing.
    :param trims:         Either a list of 2-tuples, or one tuple of 2 ints.

        Empty slicing must represented with a ``0``.
            ``src[:10]+src[-5:]`` must be entered as ``trims=[(0,10), (-5,0)]``.

        Single frame slices must be represented as a normal slice.
            ``src[15]`` must be entered as ``trims=(15,16)``.
    :param audio_file:    A string or ``Path`` refering to the source audio file's location
                          (i.e. '/path/to/audio_file.wav').
                          Can also be a container file that uses a slice-able audio codec
                          such as a remuxed BDMV source into a `.mkv` file with FLAC / PCM audio.
    :param outfile:       Either a filename 'out.mka' or a full path '/path/to/out.mka'
                          that will be used for the trimmed audio file.
                          If left empty, will default to ``audio_file`` + ``_cut.mka`` (Default: ``None``).
    :param mkvmerge_path: Set this if ``mkvmerge`` is not in your `PATH`
                          or if you want to use a portable executable (Default: ``None``).

    :param ffmpeg_path: Needed to output a `.wav` track instead of a one-track Mastroka Audio file (Default: ``None``).

        If ``ffmpeg`` exists in your `PATH`, it will automatically be detected and used.

        If set to ``None`` or ``ffmpeg`` can't be found, will only output a `.mka` file.

        If specified as a blank string ``''``, the script will skip attemping to re-write the file as a `.wav` track
        and will simply output a `.mka` file.
    :param quiet:         Suppresses most console output from MKVToolNix and FFmpeg (Default: ``False``).
    :param debug:         Used for testing purposes (Default: ``False``).

    :return: If ``debug`` is ``True``, returns a dictionary of values for testing, otherwise returns ``None``.

        Outputs a cut/spliced audio file in either the script's directoy or the path specified with ``outfile``.
    """
    if not mkvmerge_path:
        if not (mkvmerge_path := which('mkvmerge')):
            raise FileNotFoundError('eztrim: mkvmerge executable not found')

    audio_file = Path(audio_file)
    if not audio_file.exists():
        raise FileNotFoundError('eztrim: {audio_file} not found')

    if not outfile:
        outfile = Path(os.path.splitext(audio_file)[0] + '_cut.mka')
    else:
        outfile = Path(outfile)
        if os.path.splitext(outfile)[1] != '.mka':
            warn('eztrim: outfile does not have a `.mka` extension, one will be added for you', SyntaxWarning)
            outfile = Path(os.path.splitext(outfile)[0] + '.mka')

    # error checking
    if not isinstance(trims, (list, tuple)):
        raise TypeError('eztrim: trims must be a list of 2-tuples (or just one 2-tuple)')
    if len(trims) == 1 and isinstance(trims, list):
        warn('eztrim: using a list of one 2-tuple is not recommended; for a single trim, directly use a tuple: `trims=(5,-2)` instead of `trims=[(5,-2)]`', SyntaxWarning)
    if isinstance(trims, list):
        for trim in trims:
            if not isinstance(trim, tuple):
                raise TypeError('eztrim: the trim {trim} is not a tuple')
            if len(trim) != 2:
                raise ValueError('eztrim: the trim {trim} needs 2 elements')
            for i in trim:
                if not isinstance(i, int):
                    raise ValueError('eztrim: the trim {trim} must have 2 ints')

    if isinstance(trims, tuple):
        if len(trims) != 2:
            raise ValueError('eztrim: the trim must have 2 elements')
        start: int = trims[0]
        end: int = trims[1]  # directly un-pack values from the single trim
        start, end = cast(Tuple, _negative_to_positive(clip, start, end))
        if end <= start:
            raise ValueError('eztrim: the trim {trims} is not logical')
        cut_ts_s: List[str] = [_f2ts(clip, start)]
        cut_ts_e: List[str] = [_f2ts(clip, end)]
    else:
        starts: List[int] = [s for s, e in trims]
        ends: List[int] = [e for s, e in trims]
        starts, ends = cast(Tuple, _negative_to_positive(clip, starts, ends))
        if _check_ordered(starts, ends):
            cut_ts_s = [_f2ts(clip, f) for f in starts]
            cut_ts_e = [_f2ts(clip, f) for f in ends]
        else:
            raise ValueError('eztrim: the trims are not logical')

    if debug:
        if isinstance(trims, list):
            return {'s': starts, 'e': ends, 'cut_ts_s': cut_ts_s, 'cut_ts_e': cut_ts_e}
        elif isinstance(trims, tuple):
            return {'s': start, 'e': end, 'cut_ts_s': cut_ts_s, 'cut_ts_e': cut_ts_e}

    delay_statement = []

    split_parts = 'parts:'
    for s, e in zip(cut_ts_s, cut_ts_e):
        split_parts += f'{s}-{e},+'

    split_parts = split_parts[:-2]

    identify_proc = run([mkvmerge_path, '--output-charset', 'utf-8', '--identify', str(audio_file)], text=True, check=True, stdout=PIPE, encoding='utf-8')
    identify_pattern = compile(r'Track ID (\d+): audio')
    if re_return_proc := identify_pattern.search(identify_proc.stdout) if identify_proc.stdout else None:
        tid = re_return_proc.group(1) if re_return_proc else '0'

        filename_delay_pattern = compile(r'DELAY ([-]?\d+)', flags=IGNORECASE)
        re_return_filename = filename_delay_pattern.search(str(audio_file))

        delay_statement = ['--sync', f'{tid}:{re_return_filename.group(1)}'] if (tid and re_return_filename) else []

    mkvmerge_silence = ['--quiet'] if quiet else []
    cut_args = [str(mkvmerge_path)] + mkvmerge_silence + ['-o', str(outfile)] +  delay_statement + ['--split', split_parts, '-D', '-S', '-B', '-M', '-T', '--no-global-tags', '--no-chapters', str(audio_file)]
    run(cut_args)

    if ffmpeg_path is None:
        ffmpeg_path = which('ffmpeg')

    if ffmpeg_path:
        ffmpeg_silence = ['-loglevel', '16'] if quiet else []
        run([str(ffmpeg_path), '-hide_banner'] + ffmpeg_silence + ['-i', str(outfile), os.path.splitext(outfile)[0] + '.wav'])
        os.remove(outfile)

    return None


def _f2ts(clip: vs.VideoNode, f: int) -> str:
    """Converts frame number to HH:mm:ss.nnnnnnnnn timestamp based on clip's framerate."""
    t = round(10 ** 9 * f * clip.fps ** -1)

    s = t / 10 ** 9
    m = s // 60
    s %= 60
    h = m // 60
    m %= 60

    return f'{h:02.0f}:{m:02.0f}:{s:012.9f}'


def _negative_to_positive(clip: vs.VideoNode, a: Union[List[int], int], b: Union[List[int], int]) \
        -> Union[Tuple[List[int], List[int]], Tuple[int, int]]:
    """Changes negative/zero index to positive based on clip.num_frames."""
    num_frames = clip.num_frames

    # speed-up analysis of a single trim
    if isinstance(a, int) and isinstance(b, int):
        if abs(a) > num_frames or abs(b) > num_frames:
            raise ValueError('_negative_to_positive: {max(abs(a), abs(b))} is out of bounds')
        return a if a >= 0 else num_frames + a, b if b > 0 else num_frames + b

    else:
        a = cast(List, a)
        b = cast(List, b)
        if len(a) != len(b):
            raise ValueError('_negative_to_positive: lists must be same length')

        for x, y in zip(a, b):
            if abs(x) > num_frames or abs(y) > num_frames:
                raise ValueError('_negative_to_positive: {max(abs(x), abs(y))} is out of bounds')

        if all(i >= 0 for i in a) and all(i > 0 for i in b): return a, b

        positive_a = [x if x >= 0 else num_frames + x for x in a]
        positive_b = [y if y > 0 else num_frames + y for y in b]

        return positive_a, positive_b


# Static helper functions
def _check_ordered(a: List[int], b: List[int]) -> bool:
    """Checks if lists follow logical python slicing."""
    if len(a) != len(b):
        raise ValueError('_check_ordered: lists must be same length')
    if len(a) == 1 and len(b) == 1:
        if a[0] >= b[0]:
            return False

    if not all(a[i] < a[i + 1] for i in range(len(a) - 1)):
        return False  # checks if list a is ordered L to G
    if not all(b[i] < a[i + 1] for i in range(len(a) - 1)):
        return False  # checks if all ends are less than next start
    if not all(a[i] < b[i] for i in range(len(a))):
        return False  # makes sure pair is at least one frame long

    return True
