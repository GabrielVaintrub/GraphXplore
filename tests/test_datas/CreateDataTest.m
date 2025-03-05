clear;
clc;

% Définir le chemin par défaut contenant vos fichiers s2p
DefaultFilesPath = 'C:\Users\vaintrug\OneDrive - Université Savoie Mont Blanc\Documents\_CROMA\Donnees_Simu\Comparaison_Calculs_HFSS';

% Charger les fichiers s2p
[DatasFiles.Names, DatasFiles.Paths] = LoadFiles(DefaultFilesPath, 'on', 'Selection données s2p', '*.s2p');
nbfiles = size(DatasFiles.Names, 2);

datas = cell(nbfiles,1);
for index_file = 1:nbfiles
    sparams = sparameters(fullfile(DatasFiles.Paths{index_file}, DatasFiles.Names{index_file}));
    content.fileName = DatasFiles.Names{index_file};
    content.filePath = DatasFiles.Paths{index_file};

    content.main_display_vector.name = 'Frequencies';
    content.main_display_vector.units = 'Hz';
    content.main_display_vector.values = sparams.Frequencies;

    content.values.absS11 = squeeze(abs(sparams.Parameters(1, 1, :)));
    content.values.absS21 = squeeze(abs(sparams.Parameters(1, 2, :)));
    content.values.absS12 = squeeze(abs(sparams.Parameters(2, 1, :)));
    content.values.absS22 = squeeze(abs(sparams.Parameters(2, 2, :)));
        
    content.values.angleS11 = squeeze(angle(sparams.Parameters(1, 1, :)));
    content.values.angleS12 = squeeze(angle(sparams.Parameters(1, 2, :)));
    content.values.angleS21 = squeeze(angle(sparams.Parameters(2, 1, :)));
    content.values.angleS22 = squeeze(angle(sparams.Parameters(2, 2, :)));

    % content.values
    content.parameters = GetOneFileParams(DatasFiles.Names{index_file}, InitSetUpFiles());
    datas{index_file} = content;
end


save('dataTable.mat', 'datas');


function SetUpFile = InitSetUpFiles()
    NumParam = 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'Lot';
    
    NumParam = NumParam + 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'Parametre';
    
    NumParam = NumParam + 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'Deembeding';
    SetUpFile(NumParam).Sufix = 'Deembed';
    
    
    NumParam = NumParam + 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'FacePort';
    SetUpFile(NumParam).Prefix = 'FacePort';
    
    NumParam = NumParam + 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'Line length';
    SetUpFile(NumParam).Prefix = 'L';
    SetUpFile(NumParam).Sufix = 'um';
    
    NumParam = NumParam + 1;
    SetUpFile(NumParam) = FileParam;
    SetUpFile(NumParam).Name = 'Port width';
    SetUpFile(NumParam).Prefix = 'P';
    SetUpFile(NumParam).Sufix = 'um';

end

