# src/data/importer.py
import os
import scipy.io as sio
import numpy as np

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
    file_name = os.path.basename(path)
    try:
        mat_data = sio.loadmat(path, squeeze_me=True)
        # Ici, nous supposons que la table a été sauvegardée sous le nom 'T'
        if 'datas' in mat_data:
            datas = mat_data['datas']
            if is_matlab_datas(datas):
                # On ajoute dans current_data un dictionnaire contenant le nom, le chemin et la table
                current_data.append({
                    'fileName': file_name,
                    'filePath': path,
                    'dataTable': datas
                })
                messages.append(f"Fichier importé : {file_name}")
            else:
                # messages.append(f"Le fichier {file_name} ne contient pas une table valide.")
                return
        else:
            messages.append(f"Le fichier {file_name} ne contient pas de variable 'T'.")
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
    """
    Vérifie heuristiquement si l'objet chargé depuis le fichier .mat
    correspond au format attendu : un cell array (ou numpy.ndarray converti en liste)
    de structures (sous forme de dictionnaires) contenant au moins les champs :
      - fileName
      - filePath
      - frequencies
      - values (contenant par exemple absS11, absS21, absS12, absS22, angleS11, angleS12, angleS21, angleS22)
      - parameters
    """
    try:
        # print(type(obj))

        # Si l'objet est un numpy.ndarray, le convertir en liste.
        # if isinstance(obj, np.ndarray):
        #     obj = obj.tolist()
        #     print("Conversion de numpy.ndarray en liste")
        
        # if not isinstance(obj, (list, tuple)):
        #     print("Erreur: l'objet n'est pas une liste ou un tuple.")
        #     return False
        if len(obj) == 0:
            print("Erreur: l'objet est vide.")
            return False
        first = obj[0]
        print("Type du premier element de la donnée :", type(first))
        # print("Contenu du premier element de la donnée :", first)
        fields = first.dtype
        print("Champs : ", fields[0].ObjectDType)
        print("Champs 0 value:", obj[0]['fileName'])
        # print("Contenu après extraction :", first_items)        
        
         # S'il s'agit d'un tuple, le convertir en dictionnaire
        # if isinstance(first, tuple):
        #     first_converted = convert_tuple_to_dict(first)
        #     if first_converted is None:
        #         print("Erreur: Impossible de convertir le tuple en dictionnaire.")
        #         return False
        #     else:
        #         first = first_converted
        #         print("Premier élément converti en dictionnaire:", first)
        # elif not isinstance(first, dict):
        #     print("Erreur: Le premier élément n'est ni un dictionnaire ni un tuple.")
        #     return False
        
        # # Vérifier la présence des champs obligatoires
        # required_fields = ['fileName', 'filePath', 'frequencies', 'values', 'parameters']
        # for field in required_fields:
        #     if field not in first:
        #         print(f"Erreur: Champ manquant dans le dictionnaire: {field}")
        #         return False
        
        # # Vérifier que 'values' est un dictionnaire et contient au moins un sous-champ attendu
        # if not isinstance(first['values'], dict):
        #     print("Erreur: Le champ 'values' n'est pas un dictionnaire.")
        #     return False
        # sub_fields = ['absS11', 'absS21', 'absS12', 'absS22', 
        #               'angleS11', 'angleS12', 'angleS21', 'angleS22']
        # if not any(sub in first['values'] for sub in sub_fields):
        #     print("Erreur: Aucun sous-champ attendu trouvé dans 'values'.")
        #     return False
        
        # print("Vérification réussie: l'objet semble correspondre au format attendu.")
        # return True
    except Exception as e:
        print("Exception dans is_matlab_datas:", e)
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

def convert_tuple_to_dict(t):
    """
    Convertit un tuple en dictionnaire en supposant que l'ordre des éléments
    est : fileName, filePath, frequencies, values, parameters.
    Si le tuple ne contient pas assez d'éléments, retourne None.
    """
    keys = ['fileName', 'filePath', 'frequencies', 'values', 'parameters']
    if len(t) < len(keys):
        print("Erreur: le tuple ne contient pas suffisamment d'éléments.")
        return None
    return {keys[i]: t[i] for i in range(len(keys))}
