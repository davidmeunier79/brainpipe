import numpy as np

__all__ = ['binarize',
           'binArray',
           'p2str',
           'list2index',
           'groupInList',
           'ndsplit',
           'ndjoin',
           'squarefreq'
           ]


def binarize(starttime, endtime, width, step, kind='tuple'):
    """Generate a window to binarize a signal

    starttime : int
        Start at "starttime"

    endtime : int
        End at "endtime"

    width : int, optional [def : None]
        width of a single window

    step : int, optional [def : None]
        Each window will be spaced by the "step" value

    kind : string, optional, [def: 'list']
        Return either a list or a tuple
    """
    X = np.vstack((np.arange(starttime, endtime-width+step, step),
                  np.arange(starttime+width, endtime+step, step)))
    if X[1, -1] > endtime:
        X = X[:, 0:-1]
    if kind == 'array':
        return X
    if kind == 'list':
        return [[X[0][k], X[1][k]] for k in range(X.shape[1])]
    elif kind == 'tuple':
        return [(X[0][k], X[1][k]) for k in range(X.shape[1])]


def binArray(x, binList, axis=0):
    """Binarize an array

    x : array
        Array to binarize

    binList : list of tuple/list
        This list contain the index to binarize the array x

    axis : int, optional, [def: 0]
        Binarize along the axis "axis"

    -> Return the binarize x and the center of each window.
    """
    nbin = len(binList)
    x = np.swapaxes(x, 0, axis)

    xBin = np.zeros((nbin,)+x.shape[1::])
    for k, i in enumerate(binList):
        if i[1] - i[0] == 1:
            xBin[k, ...] = x[i[0], ...]
        else:
            xBin[k, ...] = np.mean(x[i[0]:i[1], ...], 0)

    return np.swapaxes(xBin, 0, axis), [(k[0]+k[1])/2 for k in binList]


def p2str(p):
    """Convert a pvalue to a string. Usefull for saving !
    """
    pStr = str(p)
    return pStr[-1]+'e-'+str(len(pStr[pStr.find('.')+1::]))


def list2index(dim1, dim2):
    """From two dimensions dim1 and dim2, build a list of
    tuple which combine this two list
    Example:
    for (2,3) -> [(0,0),(1,0),(0,1),(1,1),(0,2),(1,2)]
    """
    list1 = list(np.arange(dim1))*dim2
    list2 = sum([[k]*dim1 for k in range(dim2)], [])
    return list(zip(list1, list2)), list1, list2


def groupInList(x, idx):
    """Group elements in an array/list using a list of index
    Example:
    groupInList([1,2,3,4,5],[0,0,1,1,2]) = [[1,2],[3,4],[5]]
    """
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if not isinstance(idx, list):
        idx = list(idx)
    # Get the list of unique elements in idx:
    uelmt = list(set(idx))
    idx = np.array(idx)
    return [list(x[np.where(idx == k)]) for k in uelmt]


def ndsplit(x, sp, axis=0):
    """Split array (work for odd dimensions)

    Args:
        x: array
            Data to split

        sp: int
            Number of chunk

    Kargs:
        axis: int, optional, [def: 0]
            Axis for splitting array

    Return:
        List of splitted arrays
    """
    # Check dimensions :
    sz = x.shape[axis]%sp
    if axis != 0:
        x = np.swapaxes(x, 0, axis)
    dim = x.shape
    if sp <= dim[0]:
        # First split :
        xs = np.split(x[0:dim[0]-sz, ...], sp, axis=0)
        # Complete list with undivisibale data :
        if sz != 0:
            m_end = xs[-1]
            xs.pop(-1)
            mat = np.concatenate((m_end, x[-sz::, ...]), axis=0)
            xs.append(mat)
        return xs
    else:
        import warnings
        warnings.warn("The split parameter is superior to the value "
                      "of axis "+str(axis)+". Splitting with sp=1")
        return list(x[:, np.newaxis, ...])


def ndjoin(x, axis=0):
    """Join arrays in a list

    Args:
        x: list
            List of data.

    Kargs:
        axis: optional, [def: 0]
            Axis to join arrays

    Return:
        Array
    """
    # Shape scanning:
    xj = np.array([])
    for num, k in enumerate(x):
        try:
            xj = np.concatenate((xj, k), axis=axis) if xj.size else k
        except:
            raise ValueError("Element "+str(num)+" is not consistent.")
    return xj


def squarefreq(fstart, fend, fwidth):
    """Build a square frequency vector.

    Args:
        fstart: int
            Starting frequency

        fend: int
            Ending frequency

        fwidth: int
            Width between each frequency

    Return:
        fce: list
            List of frequencies.
    """
    fce = []
    refce = np.arange(fstart, fend+fwidth, fwidth)
    [[fce.append([k, i]) for i in refce[num+1::]] for num, k in enumerate(refce)]
    return fce
