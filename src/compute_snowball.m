hdf5_path = ['/beegfs/vl1019/spl2017_data/BirdVox-70k_hdf5/' ...
    'original/BirdVox-70k_original_unit01.hdf5'];
Q = 16;

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
Q_str = sprintf('%02d', Q);
disp(['Quality factor (Q): ', Q_str, '.']);
disp(['Unit: ', unit_str, '.'])
disp(['Augmentation: ', instanced_aug_str, '.']);
disp(['Number of files: ', sprintf('%d', n_waveform_names), '.']);

waveform_name_id = 1;
waveform_name = waveform_names{waveform_name_id};
waveform_path = ['/waveforms/', waveform_name];
