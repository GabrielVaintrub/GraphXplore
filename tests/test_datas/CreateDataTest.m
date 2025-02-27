clear;
clc;

% Définir le chemin par défaut contenant vos fichiers s2p
DefaultFilesPath = 'C:\Users\vaintrug\OneDrive - Université Savoie Mont Blanc\Documents\_CROMA\Donnees_Simu\Comparaison_Calculs_HFSS';

% Charger les fichiers s2p
[DatasFiles.Names, DatasFiles.Paths] = LoadFiles(DefaultFilesPath, 'on', 'Selection données s2p', '*.s2p');
nbfiles = size(DatasFiles.Names, 2);

% Créer une container map globale pour stocker les données de tous les dispositifs
dataMap = containers.Map();

% Boucle sur tous les fichiers
for index_file = 1:nbfiles
    % Créer une map pour le fichier courant
    filemap = containers.Map();
    
    % Charger les paramètres S du fichier courant
    sparams = sparameters(fullfile(DatasFiles.Paths{index_file}, DatasFiles.Names{index_file}));
    
    % Stocker diverses informations dans la map
    filemap('fileName')      = DatasFiles.Names{index_file};
    filemap('filePaths')     = DatasFiles.Paths{index_file};
    filemap('frequences')    = sparams.Frequencies;
    filemap('absS11')        = abs(sparams.Parameters(1, 1, :));
    filemap('absS21')        = abs(sparams.Parameters(2, 1, :));
    filemap('absS12')        = abs(sparams.Parameters(1, 2, :));
    filemap('absS22')        = abs(sparams.Parameters(2, 2, :));
    filemap('angleS11')      = angle(sparams.Parameters(1, 1, :));
    filemap('angleS21')      = angle(sparams.Parameters(2, 1, :));
    filemap('angleS12')      = angle(sparams.Parameters(1, 2, :));
    filemap('angleS22')      = angle(sparams.Parameters(2, 2, :));
    
    % Ajouter la map du fichier courant à la map globale, indexée par le nom du fichier
    dataMap(filemap('fileName')) = filemap;
end

% Sauvegarder la container map globale dans un fichier .mat
save('dataMap.mat', 'dataMap');
