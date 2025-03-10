function exportDataToJson(data)
    % EXPORTDATATOJSON Exporte les données MATLAB au format JSON.
    % La fonction reçoit directement la variable data et crée un fichier JSON
    % nommé "exported_data.json" dans le répertoire courant.
    %
    % Exemple d'utilisation :
    %   data = load('monFichier.mat', '-mat');
    %   exportDataToJson(data);
    
    % Convertir la variable data en JSON avec une mise en forme lisible
    jsonStr = jsonencode(data, 'PrettyPrint', true);
    
    % Définir le chemin de sortie (ici, dans le répertoire courant)
    jsonFilePath = fullfile(pwd, 'exported_data.json');
    
    % Ouvrir le fichier en écriture avec l'encodage UTF-8
    fid = fopen(jsonFilePath, 'w', 'n', 'UTF-8');
    if fid == -1
        error('Impossible d''ouvrir le fichier %s pour écriture.', jsonFilePath);
    end
    
    % Écrire la chaîne JSON dans le fichier
    fwrite(fid, jsonStr, 'char');
    fclose(fid);
    
    fprintf('Données exportées dans le fichier %s\n', jsonFilePath);
end
