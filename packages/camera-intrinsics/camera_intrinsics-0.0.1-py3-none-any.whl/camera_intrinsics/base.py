from typing import Optional
from copy import copy


def check_intrinsics(intrinsics: dict) -> bool:
    """Check if given intrinsics are valid.

    Parameters
    ----------
    intrinsics : dict
        The intrinsics to be checked.

    Returns
    -------
    bool
        Flag if the intrinsics are valid.
    """

    return intrinsics.get("options", None) == ""


def check_intrinsics_msg(intrinsics: dict) -> str:
    """Check if given intrinsics are valid.

    Parameters
    ----------
    intrinsics : dict
        The intrinsics to be checked.

    Returns
    -------
    bool
        Flag if the intrinsics are valid.
    """

    if intrinsics.get("options", None) != "":
        return f"Currently only empty options are supported. intrinsics['options'] = '{intrinsics['options']}'."


def intrinsics(width: int, height: int, fx: float, fy: float, cx: float, cy: float, half_pixel_centers: bool = False) -> dict:
    """Generate new camera intrinsics.

    Parameters
    ----------
    width : int
        The width of the image.
    height : int
        The height of the image.
    fx : float
        The x-axis focal length of the camera in pixels.
    fy : float
        The y-axis focal length of the camera in pixels.
    cx : float
        The x-axis optical center of the camera in pixels.
    cy : float
        The y-axis optical center of the camera in pixels.
    half_pixel_centers : bool, optional
        Controls the coordinate system used for the pixels, by default False.
            True:   The coordinates of the middle of the top left pixels are (x=0.5, y=0.5).
                    This convention is used by e.g. COLMAP
            False:  The coordinates of the middle of the top left pixels are (x=0, y=0).
                    This is the preferred convention and used by e.g. DSO, Matplotlib, or the Matlab calib toolbox

    Returns
    -------
    dict
        The camera intrinsics as a dict with the following keys: height, width, fx, fy, cx, cy, options.
        Options is a string that encodes e.g. the half_pixel_center attribute.
    """

    return {
        'height': int(height),
        'width': int(width),
        'fx': float(fx),
        'fy': float(fy),
        'cx': float(cx),
        'cy': float(cy),
        'options': "half_pixel_centers" if half_pixel_centers else ""
    }


def _intrinsics(width: int, height: int, fx: float, fy: float, cx: float, cy: float, options: str):
    opt = options.split(",")
    if 'half_pixel_centers' in opt:
        cx = cx + 0.5
        cy = cy + 0.5

    return {
        'height': int(height),
        'width': int(width),
        'fx': float(fx),
        'fy': float(fy),
        'cx': float(cx),
        'cy': float(cy),
        'options': options
    }


def _width(intrinsics: dict) -> int:
    return intrinsics['width']


def _height(intrinsics: dict) -> int:
    return intrinsics['height']


def _fx(intrinsics: dict) -> float:
    return intrinsics['fx']


def _fy(intrinsics: dict) -> float:
    return intrinsics['fy']


def _cx(intrinsics: dict) -> float:
    cx = intrinsics['cx']
    if 'half_pixel_centers' in _options(intrinsics):
        cx = cx - 0.5
    return cx


def _cy(intrinsics: dict) -> float:
    cy = intrinsics['cy']
    if 'half_pixel_centers' in _options(intrinsics):
        cy = cy - 0.5
    return cy


def _options(intrinsics: dict) -> list:
    return intrinsics['options'].split(",")


def crop(intrinsics: dict, width: int, height: int, col: int, row: int) -> dict:
    """Intrinsics after cropping.

    Parameters
    ----------
    intrinsics : dict
        The camera intrinsics of the original image.
    width : int
        The width of the cropped image.
    height : int
        The height of the cropped image.
    col : int
        Left column index for cropping.
    row : int
        Upper row index for cropping.

    Returns
    -------
    dict
        The camera intrinsics of the cropped image.
    """

    return _intrinsics(
        width=width,
        height=height,
        fx=_fx(intrinsics),
        fy=_fy(intrinsics),
        cx=_cx(intrinsics) - col,
        cy=_cy(intrinsics) - row,
        options=intrinsics['options']
    )


def resize(intrinsics: dict, width: int, height: int) -> dict:
    """Intrinsics after resizing.

    Parameters
    ----------
    intrinsics : dict
        The camera intrinsics of the original image.
    width : int
        The width of the resized image.
    height : int
        The height of the resized image.

    Returns
    -------
    dict
        The camera intrinsics of the resized image.
    """

    cx_hpc = _cx(intrinsics) + 0.5
    cy_hpc = _cy(intrinsics) + 0.5

    cx_hpc_new = cx_hpc / float(_width(intrinsics)) * width
    cy_hpc_new = cy_hpc / float(_height(intrinsics)) * height

    cx_new = cx_hpc_new - 0.5
    cy_new = cy_hpc_new - 0.5

    return _intrinsics(
        width=width,
        height=height,
        fx=_fx(intrinsics),
        fy=_fy(intrinsics),
        cx=cx_new,
        cy=cy_new,
        options=intrinsics['options']
    )
