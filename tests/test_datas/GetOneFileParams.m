function [FileParams] = GetOneFileParams(FileName, SetUpFile, Delimiter)
arguments
    FileName = '';
    SetUpFile = [FileParam];
    Delimiter = '_';
end

NbParamsSetUp = width(SetUpFile);

% FileParams = repmat(FileParam, NbFiles, NbParamsSetUp); % Tableau d'objets de résultat

temp  = split(FileName, '.');
if length(temp) > 2
    Splited = "";
    for j = 1: length(temp)-2
        Splited = strcat(Splited, temp(j), ".");
    end
    Splited = strcat(Splited, temp(length(temp)-1));
    Splited = split(Splited, Delimiter);
else
    Splited = split(temp(1), Delimiter);
end
NbParamsFile = length(Splited);
NbParams = max(NbParamsSetUp, NbParamsFile);
for j = 1 : NbParamsSetUp
    if j <= NbParamsFile
        FileParams(j).Name = SetUpFile(j).Name;
        FileParams(j).Prefix = SetUpFile(j).Prefix;
        FileParams(j).Sufix = SetUpFile(j).Sufix;
        Splited{j} = erase(Splited{j}, SetUpFile(j).Prefix);
        FileParams(j).Value = erase(Splited{j}, SetUpFile(j).Sufix);
    end
end
for j = NbParamsSetUp+1 : NbParams
    if j <= NbParamsFile
        FileParams(j).Name = strcat('Param' , string(j));
        FileParams(j).Value = Splited{j};
    end
end


end
