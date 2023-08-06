"""
This Python module allows you to synchronize a whole session worth
of physiological data to the session images, so the physiological
files will be matched to the corresponding image files and named
accordingly.

The module is file type agnostic, so it can be used for AcqKnowledge
files, Eye-link files (.edf), etc. The module relies on the calling
function extracting the timing of the onsets of the different
scanner runs. The module will then find the best time delay between
the physilogical files and the imaging files.

Methods related to saving the physiological files (either as BIDS or
just compressed) are part of this module too, since the call can be
file type independent.
"""
import os
import os.path as op
from operator import itemgetter
from itertools import groupby
import tarfile
from tempfile import TemporaryDirectory
from datetime import datetime

from bids import BIDSLayout
import bioread
import pandas as pd
import numpy as np
import nibabel as nib


def compress_physio(physio_file, out_prefix, get_physio_acq_time, overwrite):
    """Archives a physiological file into a tarball

    Also it tries to do it reproducibly, so it takes the date for
    the physio_file and targets tarball based on the acquisition time

    Parameters
    ----------
    physio_file : str
      original physiological file
    out_prefix : str
      output path prefix, including the portion of the output file
      name before .*.tgz suffix
    get_physio_acq_time : function
        Function to get the acquisition time of a physiological file
        (e.g., read_file(file).earliest_marker_created_at, from bioread)
    overwrite : bool
      Overwrite existing tarfiles

    Returns
    -------
    filename : str
      Result tarball
    """

    fname, physio_extension = op.splitext(physio_file)
    outtar = out_prefix + physio_extension + '.tgz'

    if op.exists(outtar) and not overwrite:
        print("File {} already exists, will not overwrite".format(outtar))
        return
    # tarfile encodes current time.time inside, making those non-
    # reproducible, so we should use the earliest_marker_created_at
    # of the acq_file

    # return physio file acquisition time as a float (like in
    # the method time.time()):
    acq_time = get_physio_acq_time(physio_file).timestamp()

    def _assign_acq_time(ti):
        # Reset the time of the TarInfo object:
        ti.mtime = acq_time
        return ti

    # poor man mocking since can't rely on having mock
    try:
        import time
        _old_time = time.time
        time.time = lambda: acq_time
        if op.lexists(outtar):
            os.unlink(outtar)
        with tarfile.open(outtar, 'w:gz', dereference=True) as tar:
            tmpdir = TemporaryDirectory()
            outfile = op.join(tmpdir.name, op.basename(physio_file))
            if not op.islink(outfile):
                os.symlink(op.realpath(physio_file), outfile)
            # place into archive stripping any lead directories and
            # adding the one corresponding to prefix
            tar.add(outfile,
                    arcname=op.join(op.basename(out_prefix),
                                    op.basename(outfile)),
                    recursive=False,
                    filter=_assign_acq_time)
    finally:
        time.time = _old_time

    return outtar


def extract_physio_onsets(trigger_timeseries, freq, threshold=0.5):
    """
    Collect onsets from physio file, both in terms of seconds and time series
    indices.
    TODO: Stitch segments together before extracting onsets.
    """
    samplerate = 1. / freq
    scan_idx = np.where(trigger_timeseries > 0)[0]
    # Get groups of consecutive numbers in index
    groups = []
    for k, g in groupby(enumerate(scan_idx), lambda x: x[0] - x[1]):
        groups.append(list(map(itemgetter(1), g)))

    # Extract onsets
    onsets = np.array([g[0] for g in groups])
    onsets_in_sec = onsets * samplerate
    durations = np.array([g[-1] - g[0] for g in groups])
    durations_in_sec = durations * samplerate
    df = pd.DataFrame(
        columns=['onset'],
        data=onsets_in_sec,
    )
    df['index'] = onsets
    df['duration'] = durations_in_sec
    return df


def synchronize_onsets(phys_df, scan_df):
    """Find matching scans and physio trigger periods from separate DataFrames,
    using time differences within each DataFrame.

    There can be fewer physios than scans (task failed to trigger physio)
    or fewer scans than physios (aborted scans are not retained in BIDS dataset).

    Onsets are in seconds. The baseline (i.e., absolute timing) doesn't matter.
    Relative timing is all that matters.

    Parameters
    ----------
    phys_df : pandas.DataFrame
        DataFrame with onsets of physio trigger periods, in seconds. The
        baseline does not matter, so it is reasonable for the onsets to start
        with zero. The following columns are required: 'onset', 'index'.
    scan_df : pandas.DataFrame
        DataFrame with onsets and names of functional scans from BIDS dataset,
        in seconds. The baseline does not matter, so it is reasonable for the
        onsets to start with zero. The following columns are required: 'onset',
        'duration'.

    Returns
    -------
    phys_df : pandas.DataFrame
        Updated scan DataFrame, now with columns for predicted physio onsets in
        seconds and in indices of the physio trigger channel, as well as scan
        duration in units of the physio trigger channel.
    """
    phys_df = phys_df.sort_values(by=['onset'])
    scan_df = scan_df.sort_values(by=['onset'])
    scan_df.index = range(scan_df.shape[0])   # overwrite the run number

    # Get difference between each physio trigger onset and each scan onset
    onset_diffs = np.zeros((scan_df.shape[0], phys_df.shape[0]))
    for i, i_scan in scan_df.iterrows():
        for j, j_phys in phys_df.iterrows():
            onset_diff = j_phys['onset'] - i_scan['onset']
            onset_diffs[i, j] = onset_diff

    # Find the delay that gives the smallest difference between scan onsets
    # and physio onsets
    selected = (None, None)
    thresh = 1000
    for i_scan in range(onset_diffs.shape[0]):
        for j_phys in range(onset_diffs.shape[1]):
            test_offset = onset_diffs[i_scan, j_phys]
            diffs_from_phys_onset = onset_diffs - test_offset
            diffs_from_abs = np.abs(diffs_from_phys_onset)
            min_diff_row_idx = np.argmin(diffs_from_abs, axis=0)
            min_diff_col_idx = np.arange(len(min_diff_row_idx))
            min_diffs = diffs_from_abs[min_diff_row_idx, min_diff_col_idx]
            min_diff_sum = np.sum(min_diffs)
            if min_diff_sum < thresh:
                selected = (i_scan, j_phys)
                thresh = min_diff_sum
    print('Selected solution: {}'.format(selected))
    offset = onset_diffs[selected[0], selected[1]]

    # Isolate close, but negative relative onsets, to ensure scan onsets are
    # always before or at physio triggers.
    close_thresh = 2  # threshold for "close" onsets, in seconds
    diffs_from_phys_onset = onset_diffs - offset
    min_diff_row_idx = np.argmin(np.abs(diffs_from_phys_onset), axis=0)
    min_diff_col_idx = np.arange(len(min_diff_row_idx))
    min_diffs = diffs_from_phys_onset[min_diff_row_idx, min_diff_col_idx]
    min_diffs_tmp = min_diffs[abs(min_diffs) <= close_thresh]
    min_val = min(min_diffs_tmp)
    min_diffs += min_val
    offset += min_val
    print('Scan DF should be adjusted forward by {} seconds'.format(offset))

    # Find the filename of the scan the 'onset' of which is close to
    # the 'physio_onset' (if none is close enough, enter None):
    scan_df['phys_onset'] = scan_df['onset'] + offset
    scan_fnames = []
    for p_on in phys_df['onset']:
        corresponding_scan = scan_df.loc[
            abs(scan_df['phys_onset'] - p_on) < close_thresh,
            'filename'
        ]
        if len(corresponding_scan) == 0:
            scan_fnames.append(None)
        else:
            # append the scan filename
            scan_fnames.append(corresponding_scan.iloc[0])

    # Add the scan filenames to the phys_df:
    phys_df['scan_fname'] = [sf for sf in scan_fnames]
    return phys_df


def split_physio(physio, split_times, time_before=6, time_after=6):
    """Extract timeseries associated with each scan.
    Key in dict is scan name or physio filename and value is physio data in
    some format.
    Uses the onsets, durations, and filenames from scan_df, and the time series
    data from physio_file.

    Parameters
    ----------
    physio_file : BlueprintInput
    split_times : list of tuple
    time_before : float
        Amount of time, in seconds, to retain in physio time series *before*
        scan.
    time_after : float
        Amount of time, in seconds, to retain in physio time series *after*
        scan.

    Returns
    -------
    physio_data_dict : dict
        Dictionary containing physio run names as keys and associated segments
        as values.
    """
    pass


def save_physio(fn, physio_data):
    """Save split physio data to BIDS dataset.
    """
    pass


def determine_scan_durations(layout, scan_df, sub, ses):
    """Extract scan durations by loading fMRI files/metadata and
    multiplying TR by number of volumes. This can be used to determine the
    endpoints for the physio files.

    Parameters
    ----------
    layout : bids.layout.BIDSLayout
        Dataset layout. Used to identify functional scans and load them to
        determine scan durations.
    scan_df : pandas.DataFrame
        Scans DataFrame containing functional scan filenames and onset times.

    Returns
    -------
    scan_df : pandas.DataFrame
        Updated DataFrame with new "duration" column. Calculated durations are
        in seconds.
    """
    # TODO: parse entities in func files for searches instead of larger search.
    func_files = layout.get(datatype='func', suffix='bold',
                            extension=['nii.gz', 'nii'],
                            sub=sub, ses=ses)
    scan_df['duration'] = None
    for func_file in func_files:
        filename = op.join('func', func_file.filename)
        if filename in scan_df['filename'].values:
            n_vols = nib.load(func_file.path).shape[3]
            tr = func_file.get_metadata()['RepetitionTime']
            duration = n_vols * tr
            scan_df.loc[scan_df['filename'] == filename, 'duration'] = duration
        else:
            print('Skipping {}'.format(filename))
    return scan_df


def load_scan_data(layout, sub, ses):
    """Load timing (start time and duration) of the functional runs.
    Start times are relative to the start of the first run.

    Parameters
    ----------
    layout : bids.layout.BIDSLayout
        Dataset layout. Used to identify functional scans and load them to
        determine scan durations.
    sub : str
        Subject ID
    ses : str
        Session ID

    Returns
    -------
    scan_df : pandas.DataFrame
        Updated DataFrame with new "duration" column. Calculated durations are
        in seconds.
    """
    # Collect acquisition times:

    # scans_file = layout.get(extension='tsv', suffix='scans', sub=sub, ses=ses)
    # # For some reason, layout.get returns all the scans.tsv files,
    # # not just the one for the specified session. So filter by ses:
    # if ses:
    #     scans_file = [f for f in scans_file if ses in f.filename]
    # df = pd.read_table(scans_file[0])
    # try:
    #     df = df.drop(['operator','randstr'], axis=1)
    # except:
    #     pass

    # NOTE: Will be replaced with scans file if heudiconv makes the change
    # NOTE: Currently keeping echo in to work around bug. Basically echoes are
    # acquired at slightly different times, so we need to get the min
    # AcquisitionTime across multi-contrast scans like multi-echo at this step.
    img_files = layout.get(datatype='func', suffix='bold',
                           extension=['nii.gz', 'nii'],
                           sub=sub, ses=ses)
    df = pd.DataFrame(columns=['filename', 'acq_time'])
    for i, img_file in enumerate(img_files):
        df.loc[i, 'filename'] = op.join('func', img_file.filename)
        df.loc[i, 'acq_time'] = img_file.get_metadata()['AcquisitionTime']

    # Now back to general-purpose code
    df = determine_scan_durations(layout, df, sub=sub, ses=ses)
    df = df.dropna(subset=['duration'])  # limit to relevant scans
    # TODO: Drop duplicates at second-level resolution. Because echoes are
    # acquired at ever-so-slightly different times.
    df = df.drop_duplicates(subset=['acq_time'])  # for multi-contrast scans

    # Convert scan times to relative onsets (first scan is at 0 seconds)
    df['acq_time'] = pd.to_datetime(df['acq_time'])
    df = df.sort_values(by='acq_time')
    df['onset'] = (df['acq_time'] - df['acq_time'].min())
    df['onset'] = df['onset'].dt.total_seconds()
    return df


def convert_session(physio_files, bids_dir, sub, ses=None,
                    get_physio_acq_time=None,
                    outdir=None, save_physio_file=None,
                    overwrite=False):
    """Function to save the physiology data in a given folder as BIDS,
    matching the filenames from the study imaging files

    Parameters
    ----------
    physio_files : list of str
        List of paths of the original physio files
    bids_dir : str
        Path to BIDS dataset
    sub : str
        Subject ID. Used to search the BIDS dataset for relevant scans.
    ses : str or None, optional
        Session ID. Used to search the BIDS dataset for relevant scans in
        longitudinal studies. Default is None.
    get_physio_acq_time : function
        Function to get the acquisition time of a physiological file
        (e.g., read_file(file).earliest_marker_created_at, from bioread)
    outdir : str
        Path to a BIDS folder where we want to store the physio data.
        Default: bids_dir
    save_physio_file : function
        function to save a single physio file
        (e.g., acq2bids, from bidsphysio.acq2bids.acq2bidsphysio)
    overwrite : bool
      Overwrite existing tarfiles
    """

    # Default out_dir is bids_dir:
    outdir = outdir or bids_dir

    file_times = [get_physio_acq_time(f) for f in physio_files]
    # relative to the first one:
    rel_file_times = [f - min(file_times) for f in file_times]

    physio_df = []
    for idx, f in enumerate(physio_files):
        physio_data = bioread.read_file(f)
        is_trigger = ['trig' in c.name.lower() for c in physio_data.channels]
        trigger_idx = np.where(is_trigger)[0]
        trigger_idx = trigger_idx[0] if len(trigger_idx) else -1
        trigger_channel = physio_data.channels[trigger_idx]
        p_df = extract_physio_onsets(trigger_channel.data,
                                     freq=trigger_channel.samples_per_second)
        # adjust for relative file time:
        p_df['onset'] = [o + rel_file_times[idx].total_seconds() for o in p_df['onset']]
        p_df['filename'] = f
        physio_df.append(p_df)

    # Concatenate all dataframes, adding the filename as key:
    physio_df = pd.concat(physio_df, keys=range(len(physio_df)))
    physio_df.index.names = [None, 'trig_number']

    # Now, for the scanner timing:
    layout = BIDSLayout(bids_dir)
    df = load_scan_data(layout, sub=sub, ses=ses)

    out_df = synchronize_onsets(physio_df, df)

    sourcedir = op.join(outdir, 'sourcedata')
    if not op.isdir(sourcedir):
        os.makedirs(sourcedir)
    sub_ses_dir = op.join('sub-' + sub, ('ses-' + str(ses)) if ses else '')

    for (phys_file, scan_file) in zip(out_df['filename'], out_df['scan_fname']):
        if scan_file:
            prefix = op.join(sub_ses_dir, scan_file.split('.nii')[0])
            outdir_ = op.join(outdir, op.dirname(prefix))
            if not op.isdir(outdir_):
                os.makedirs(outdir_)
            save_physio_file(phys_file, op.join(outdir, prefix))
            sourcedir_ = op.join(sourcedir, op.dirname(prefix))
            if not op.isdir(sourcedir_):
                os.makedirs(sourcedir_)
            compress_physio(phys_file,
                            op.join(sourcedir_, op.basename(prefix)),
                            get_physio_acq_time,
                            overwrite=overwrite)


