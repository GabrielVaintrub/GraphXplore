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

def structured_to_serializable(x):
    """
    Convertit récursivement un objet chargé de MATLAB en types Python serializables.
    - Pour un numpy.ndarray : s'il s'agit d'un scalaire (size==1), on extrait la valeur ;
      sinon, on le convertit en liste.
    - Pour un objet structuré (ayant dtype.names) : on le convertit en dictionnaire en parcourant ses champs.
    - Pour un dictionnaire, on convertit ses valeurs récursivement.
    """
    # Si x est un ndarray et de taille 1, extraire la valeur.
    if isinstance(x, np.ndarray):
        if x.size == 1:
            return structured_to_serializable(x.item())
        # Si le tableau possède des champs, on le traite comme une structure
        if x.dtype.names is not None:
            return {name: structured_to_serializable(x[name]) for name in x.dtype.names}
        # Sinon, on retourne une liste de valeurs converties
        return [structured_to_serializable(item) for item in x]
    
    # Si l'objet a des champs (par exemple, un mat_struct)
    if hasattr(x, "dtype") and x.dtype.names is not None:
        return {name: structured_to_serializable(x[name]) for name in x.dtype.names}
    
    # Si x est un dictionnaire, convertir récursivement ses valeurs
    if isinstance(x, dict):
        return {k: structured_to_serializable(v) for k, v in x.items()}
    
    # Sinon, retourner l'objet tel quel (il est déjà serializable : int, float, str, etc.)
    return x