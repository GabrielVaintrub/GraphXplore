# src/data/importer.py
import os, pprint
import scipy.io as sio
from dashboard.tabs import display_vector_dropdown_options, generate_display_vector_dropdown_options
from utils.temp_dir import __TEMP_DIR__
from utils.data_processing import structured_to_serializable
temps_files = []

def import_mat_file(path, current_data, messages):
    """
    Charge un fichier .mat et vérifie qu'il contient une table MATLAB.
    
    Arguments:
        path (str): Le chemin complet vers le fichier .mat.
        current_data (list): La liste des données importées existantes.
        messages (list): La liste des messages à afficher.
    
    Retourne:
        tuple: (current_data, messages) mis à jour.
    """
    global display_vector_dropdown_options
    file_name = os.path.basename(path)
    try:
        mat_data = sio.loadmat(path, squeeze_me=True)
        if 'datas' in mat_data:
            datas = mat_data['datas']
            current_data.append({
                    'fileName': file_name,
                    'filePath': path,
                    'dataTable': datas
            })
            temps_files.append(matfile_to_txt(datas, file_name))
            # TODO convert file content to python struct
            # TODO delete file?
            display_vector_dropdown_options = generate_display_vector_dropdown_options(datas)

        else:
            messages.append(f"Le fichier {file_name} ne contient pas de variable 'datas'.")
    except Exception as e:
        messages.append(f"Erreur lors du chargement de {file_name} : {str(e)}")
    
    return current_data, messages

def is_container_map(obj):
    """
    Vérifie de manière heuristique si l'objet ressemble à une container map.
    Pour cela, on teste s'il possède une méthode keys() et s'il contient certaines clés attendues.
    Ici, on vérifie notamment la présence de 'fileName' et 'frequences' parmi les clés.
    """
    try:
        k = obj.keys()
        expected_keys = ['fileName', 'frequences']
        if all(key in k for key in expected_keys):
            return True
    except Exception:
        pass
    return False

def is_matlab_table(obj):
    """
    Vérifie de manière heuristique si l'objet semble être une table MATLAB.
    On teste s'il possède un attribut dtype avec des champs, et si ces champs
    contiennent au moins quelques colonnes attendues (ex. 'fileName', 'filePath', 'frequencies').
    """
    try:
        if hasattr(obj, 'dtype') and obj.dtype.names is not None:
            expected_fields = ['fileName', 'filePath', 'frequencies']
            return all(field in obj.dtype.names for field in expected_fields)
    except Exception:
        pass
    return False

def is_matlab_datas(obj):
    try:
        if len(obj) == 0:
            print("Erreur: l'objet est vide.")
            return False
        first = obj[0]
        # print("Type du premier element de la donnée :", type(first))
        # print("Contenu du premier element de la donnée :", first)
        fields = first.dtype.names
        # print("Noms champs : ", fields)
        # print("Champs 0 value:", obj[0][fields[0]])

    except Exception as e:
        # print("Exception dans is_matlab_datas:", e)
        return False

def mat_struct_to_dict(matobj):
    """
    Convertit récursivement un objet mat_struct (contenant _fieldnames)
    en un dictionnaire Python.
    """
    d = {}
    for field in matobj._fieldnames:
        val = getattr(matobj, field)
        # Si la valeur est elle-même un mat_struct, on la convertit récursivement.
        if hasattr(val, '_fieldnames'):
            d[field] = mat_struct_to_dict(val)
        # Si c'est un ndarray d'objets (ex. : cell array convertie), on convertit chaque élément.
        elif isinstance(val, (list, tuple)) or (hasattr(val, 'dtype') and val.dtype == object):
            d[field] = [mat_struct_to_dict(item) if hasattr(item, '_fieldnames') else item for item in val]
        elif hasattr(val, 'dtype'):
            # Si c'est un ndarray numérique et de taille 1, on extrait la valeur.
            if val.size == 1:
                d[field] = val.item()
            else:
                d[field] = val.tolist()
        else:
            d[field] = val
    return d

def matfile_to_txt(dataTable, fileName):
    with open(os.path.join(__TEMP_DIR__, f'temp_import_{fileName}.txt'), "w", encoding="utf-8") as f:
        for data in dataTable:
            serializable_data = structured_to_serializable(data)
            # f.write(data)
            f.write("array(")
            pp = pprint.PrettyPrinter(indent=4, stream=f)
            pp.pprint(serializable_data)
            result = ", ".join(f"('{x}', 'O')" for x in data.dtype.names)
            f.write("dtype = [" + result + "]),\n\n")
    return f'temp_import_{fileName}.txt'

