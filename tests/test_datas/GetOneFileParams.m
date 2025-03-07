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
        FileParams(j).name = SetUpFile(j).name;
        FileParams(j).prefix = SetUpFile(j).prefix;
        FileParams(j).sufix = SetUpFile(j).sufix;
        FileParams(j).unit = SetUpFile(j).sufix;
        Splited{j} = erase(Splited{j}, SetUpFile(j).prefix);
        FileParams(j).value = erase(Splited{j}, SetUpFile(j).sufix);
    end
end
for j = NbParamsSetUp+1 : NbParams
    if j <= NbParamsFile
        FileParams(j).Name = strcat('Param' , string(j));
        FileParams(j).Value = Splited{j};
    end
end


end
