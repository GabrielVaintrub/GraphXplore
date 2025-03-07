import numpy as np
def convert_tuple_to_dict(t):
    """
    Convertit un tuple en dictionnaire en supposant que l'ordre des éléments
    est : fileName, filePath, frequencies, values, parameters.
    Si le tuple ne contient pas assez d'éléments, retourne None.
    """
    print (len(t))
    keys = ['fileName', 'filePath', 'frequencies', 'values', 'parameters']
    # if len(t) < len(keys):
    #     print("Erreur: le tuple ne contient pas suffisamment d'éléments.")
    #     return None
    return #{keys[i]: t[i] for i in range(len(keys))}

def structured_to_serializable(obj):
    """
    Convertit récursivement un objet chargé depuis un fichier MATLAB en types
    Python standards (dictionnaires, listes, chaînes, nombres, booléens ou None)
    pour qu'il soit JSON serializable.
    """
    # Si c'est une structure MATLAB (mat_struct)
    if hasattr(obj, '_fieldnames'):
        return {field: structured_to_serializable(getattr(obj, field)) for field in obj._fieldnames}
    
    # Si c'est un dictionnaire, traiter récursivement ses valeurs
    if isinstance(obj, dict):
        return {k: structured_to_serializable(v) for k, v in obj.items()}
    
    # Si c'est un numpy.ndarray
    if isinstance(obj, np.ndarray):
        # Si le type de donnée n'est pas objet, on peut le convertir directement en liste
        if obj.dtype.kind != 'O':
            return obj.tolist()
        # Sinon, pour les tableaux d'objets, convertir chaque élément
        return [structured_to_serializable(item) for item in obj]
    
    # Si c'est une liste ou un tuple
    if isinstance(obj, (list, tuple)):
        return [structured_to_serializable(item) for item in obj]
    
    # Si c'est un objet bytes, le décoder en chaîne
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    
    # Sinon, retourner l'objet tel quel (int, float, str, bool, None, etc.)
    return obj