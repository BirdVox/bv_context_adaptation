hdf5_path = ['/beegfs/vl1019/spl2017_data/BirdVox-70k_hdf5/' ...
    'original/BirdVox-70k_original_unit01.hdf5'];
addpath(genpath('~/scattering.m'));

% Define options for first-order scattering (time-frequency representation).
opts{1}.time.size = 8192;
% Temporal oversampling by a factor 2^1=2.
opts{1}.time.U_log2_oversampling = 1;
% Number of filters per octave.
opts{1}.time.nFilters_per_octave = 48;
% Maximum quality factor.
opts{1}.time.max_Q = 24;
% Support of the low-pass filter phi.
opts{1}.time.T = 8;
% Hard constraint on the maximum scale of the wavelets psi.
opts{1}.time.max_scale = 2048;
% Number of octaves in the wavelet filterbank.
opts{1}.time.nOctaves = 8;
opts{1}.time.gamma_bounds = [1 128];
% Disable chunking
opts{1}.time.is_chunked = false;

% Define options for low-pass filtering of time-frequency representation.
opts{2}.invariants.time.T = 32;

% Define options for second-order scattering along time.
opts{2}.banks.time.T = 8192;
% No constraint on the maximum scale.
opts{2}.banks.time.max_scale = Inf;
opts{2}.banks.time.sibling_mask_factor = Inf;

% No subsampling along log-frequencies.
opts{2}.banks.gamma.U_log2_oversampling = Inf;
opts{2}.banks.gamma.S_log2_oversampling = Inf;

archs = sc_setup(opts);


addpath(genpath('~/scattering.m'));
[hdf5_folder, hdf5_name] = fileparts(hdf5_path);
hdf5_name_split = strsplit(hdf5_name, '_');
dataset_name = hdf5_name_split{1};
instanced_aug_str = hdf5_name_split{2};
unit_str = hdf5_name_split{3};
waveforms_info = h5info(hdf5_path, '/waveforms');
waveform_names = {waveforms_info.Datasets.Name};

n_waveform_names = length(waveform_names);
sample_rate = h5read(hdf5_path, '/sample_rate');

% Print header.
disp(['Computing scattering transforms for ', ...
    dataset_name, ' augmented data.']);
disp(['Unit: ', unit_str, '.'])
disp(['Augmentation: ', instanced_aug_str, '.']);
disp(['Number of files: ', sprintf('%d', n_waveform_names), '.']);

%for waveform_name_id = 1:n_waveform_names
waveform_name_id = 1;
waveform_name = waveform_names{waveform_name_id};
waveform_path = ['/waveforms/', waveform_name];

waveform = h5read(hdf5_path, waveform_path);
waveform = waveform(1:8192);

[S, U] = sc_propagate(waveform, archs);
