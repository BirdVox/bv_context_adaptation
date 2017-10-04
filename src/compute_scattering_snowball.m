function compute_scattering_snowball(hdf5_path)
% Define options for first-order scattering (time-frequency representation).
opts{1}.time.size = 8192;
% Temporal oversampling by a factor 2^1=2.
opts{1}.time.U_log2_oversampling = 1;
opts{1}.time.S_log2_oversampling = 0;
% Number of filters per octave.
opts{1}.time.nFilters_per_octave = 48;
% Maximum quality factor.
opts{1}.time.max_Q = 24;
% Support of the low-pass filter phi.
opts{1}.time.T = 64;
% Hard constraint on the maximum scale of the wavelets psi.
opts{1}.time.max_scale = 2048;
% Number of octaves in the wavelet filterbank.
opts{1}.time.nOctaves = 8;
opts{1}.time.gamma_bounds = [1 128];
% Disable chunking
opts{1}.time.is_chunked = false;

% Define options for low-pass filtering of time-frequency representation.
opts{2}.invariants.time.T = 64;

% Define options for second-order scattering along time.
opts{2}.banks.time.T = 8192;
% No constraint on the maximum scale.
opts{2}.banks.time.max_scale = Inf;
% Only compute scales larger than 2^7.
opts{2}.banks.time.gamma_bounds = [7 Inf];
opts{2}.banks.time.sibling_mask_factor = Inf;
opts{2}.banks.time.handle = @morlet_1d;

% No subsampling along log-frequencies.
opts{2}.banks.gamma.U_log2_oversampling = Inf;
opts{2}.banks.gamma.S_log2_oversampling = Inf;
opts{2}.banks.gamma.gamma_bounds = [1 4];


% Define poolings in time and frequency.
poolings = [ ...
    2 2; ...
    2 2;
    2 4;
    2 4;
    2 8;
    2 8;
    2 16];


% Build scattering architectures.
archs = sc_setup(opts);


% List waveform names.
[hdf5_folder, hdf5_name] = fileparts(hdf5_path);
hdf5_name_split = strsplit(hdf5_name, '_');
dataset_name = hdf5_name_split{1};
instanced_aug_str = hdf5_name_split{2};
unit_str = hdf5_name_split{3};
waveforms_info = h5info(hdf5_path, '/waveforms');
waveform_names = {waveforms_info.Datasets.Name};


% Retrieve sample rate.
n_waveform_names = length(waveform_names);
sample_rate = h5read(hdf5_path, '/sample_rate');


% Initialize scattering structure.
scattering = struct();


% Create feature directory if it does not already exists.
data_dir = fileparts(fileparts(hdf5_folder));
scattering_snowball_dir = [dataset_name, '_scattering-snowball'];
scattering_snowball_dir_path = fullfile(data_dir, scattering_snowball_dir);
if ~exist(scattering_snowball_directory, 'dir')
    mkdir(scattering_snowball_dir_path);
end


% Create augmentation directory if it does not already exists.
instanced_aug_dir_path = ...
    fullfile(scattering_snowball_dir_path, instanced_aug_str);
if ~exist(instanced_aug_dir_path, 'dir')
    mkdir(instanced_aug_dir_path);
end


% Loop over waveforms.
for waveform_name_id = 1:n_waveform_names
    disp(waveform_name_id);

    % Load waveform.
    waveform_name = waveform_names{waveform_name_id};
    waveform_path = ['/waveforms/', waveform_name];
    waveform = h5read(hdf5_path, waveform_path);
    waveform = waveform(1:8192);

    % Compute scattering transform.
    U0 = initialize_U(waveform, archs{1}.banks{1});
    Y1 = U_to_Y(U0, archs{1}.banks);
    U1 = Y_to_U(Y1{end}, archs{1}.nonlinearity);
    Y2 = U_to_Y(U1, archs{2}.banks);
    S1 = Y_to_S(Y2, archs{2});
    U2 = Y_to_U(Y2{end}, archs{2}.nonlinearity);
    U2_psi = U2{1,1};
    U2_phi = U2{1,2};

    % Build structure of scattering coefficients.
    nScales = length(U2{1,1}.data);
    X = struct();
    X.S1 = single(S1.data((1+end/4):end, :));

    % Loop over scales.
    for scale_id = 1:nScales
        % Pool scattering coefficients in time and frequency.
        j = opts{2}.banks.time.gamma_bounds(1) - 1 + scale_id;
        scale_str = ['U2_j', sprintf('%02d', j)];
        U2_scale = cell(1, 1+length(U2{1,1}.data{scale_id}));
        for j_j_id = 1:length(U2{1,1}.data{scale_id})
            pooled_U2_psi = cat(3, ...
                ordfilt2(U2{1,1}.data{scale_id}{j_j_id}(:, :, 1), ...
                    poolings(scale_id, 1)*poolings(scale_id, 2), ...
                    ones(poolings(scale_id, 1), poolings(scale_id, 2))), ...
                ordfilt2(U2{1,1}.data{scale_id}{j_j_id}(:, :, 2), ...
                    poolings(scale_id, 1)*poolings(scale_id, 2), ...
                    ones(poolings(scale_id, 1), poolings(scale_id, 2))));
            U2_scale{j_j_id} = pooled_U2_psi( ...
                1:poolings(scale_id, 1):end, ...
                1:poolings(scale_id, 2):end, ...
                :);
        end
        pooled_U2_phi = ordfilt2(U2{1,2}.data{scale_id}, ...
            poolings(scale_id, 1)*poolings(scale_id, 2), ...
            ones(poolings(scale_id, 1), poolings(scale_id, 2)));
        U2_scale{end} = pooled_U2_phi( ...
            1:poolings(scale_id, 1):end, ...
            1:poolings(scale_id, 2):end);
        U2_scale = cat(3, U2_scale{:});
        U2_scale = U2_scale((1+end/4):end, 1:(end/2), :);
        X.(scale_str) = single(U2_scale);
    end

    % Store X in HDF5 container.
    scattering.(waveform_name) = X;
end


% Save
out_name = [dataset_name, '_', instanced_aug_str, '_', unit_str, '.mat'];
out_path = fullfile(instanced_aug_dir_path, out_name);
save(out_path, 'scattering', '-v7.3');

end
