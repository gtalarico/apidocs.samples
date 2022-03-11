from Autodesk.Revit.DB import BoundingBoxXYZ, XYZ


def get(elem):
    """
    Retrieves a bbox for element.
    :param elem:
    :return: BoundingBoxXYZ: centroid point
    """
    return elem.get_BoundingBox(None)


def bbox_centroid(bbox):
    """
    Retrieves centroid of a bbox.
    :param bbox:
    :return: XYZ: centroid point
    """
    centroid = XYZ(
        (bbox.Max.X - bbox.Min.X) / 2 + bbox.Min.X,
        (bbox.Max.Y - bbox.Min.Y) / 2 + bbox.Min.Y,
        (bbox.Max.Z - bbox.Min.Z) / 2 + bbox.Min.Z
    )
    return centroid


def bbox_top_left_point(element):
    """
    Retrieves left top bottom point of an element.
    :param element: bboxable element
    :return: XYZ: left top bottom bbx point
    """
    bbox = element.get_BoundingBox(None)
    if isinstance(bbox, BoundingBoxXYZ):
        return XYZ(bbox.Min.X, bbox.Max.Y, bbox.Min.Z)


def bbox_xy_zmin_points(bbox):
    """
    Retrieves bbx bottom points.
    :param bbox:
    :return: tuple
    """
    min_z = bbox.Min.Z
    return (
        XYZ(bbox.Min.X, bbox.Min.Y, min_z),
        XYZ(bbox.Max.X, bbox.Min.Y, min_z),
        XYZ(bbox.Max.X, bbox.Max.Y, min_z),
        XYZ(bbox.Min.X, bbox.Max.Y, min_z),
    )


def get_bbx_from_pts(points):
    """
    Returns the bbx from a collection of points.
    :param bbox:
    :return: BoundingBox
    """
    if len(points) < 2:
        print("not enough points for bbx")
        return

    bbox = BoundingBoxXYZ()
    coord_vals = {
        "X": set(),
        "Y": set(),
        "Z": set(),
    }

    for pt in points:
        coord_vals["X"].add(getattr(pt, "X"))
        coord_vals["Y"].add(getattr(pt, "Y"))
        coord_vals["Z"].add(getattr(pt, "Z"))

    bbox.Min = XYZ(
        min(coord_vals["X"]),
        min(coord_vals["Y"]),
        min(coord_vals["Z"])
    )
    bbox.Max = XYZ(
        max(coord_vals["X"]),
        max(coord_vals["Y"]),
        max(coord_vals["Z"])
    )
    return bbox


def bbox_offset(bbox, offset):
    """
    Offsets a given bbox by an offset value.
    :param bbox:
    :param offset:
    :return: BoundingBox
    """
    offset_bbox = BoundingBoxXYZ()
    offset_bbox.Min = XYZ(
        bbox.Min.X - offset,
        bbox.Min.Y - offset,
        bbox.Min.Z - offset,
    )
    offset_bbox.Max = XYZ(
        bbox.Max.X + offset,
        bbox.Max.Y + offset,
        bbox.Max.Z + offset,
    )
    return offset_bbox


def get_combined_bbox(bboxes):
    """
    Combines given bboxes into union bbox
    :param bboxes:
    :return: BoundingBox: combined_bbox
    """
    combined_bbox = BoundingBoxXYZ()

    min_xs = set()
    min_ys = set()
    min_zs = set()
    max_xs = set()
    max_ys = set()
    max_zs = set()

    for bbox in bboxes:
        min_xs.add(bbox.Min.X)
        min_ys.add(bbox.Min.Y)
        min_zs.add(bbox.Min.Z)
        max_xs.add(bbox.Max.X)
        max_ys.add(bbox.Max.Y)
        max_zs.add(bbox.Max.Z)

    combined_bbox.Min = XYZ(
        min(min_xs),
        min(min_ys),
        min(min_zs),
    )
    combined_bbox.Max = XYZ(
        max(max_xs),
        max(max_ys),
        max(max_zs),
    )

    return combined_bbox


def bboxes_overlap(bbox_a, bbox_b):
    """
    check if two given bboxes overlap
    :param bboxes:
    :return: BoundingBox: intersecting_bbox
    """
    directions = {"X": False, "Y": False, "Z": False}
    for direction in directions:
        a_max = getattr(bbox_a.Max, direction)
        a_min = getattr(bbox_a.Min, direction)
        b_max = getattr(bbox_b.Max, direction)
        b_min = getattr(bbox_b.Min, direction)
        # print(a_min, a_max, b_min, b_max)
        a_before_b = a_min <= b_min and a_max <= b_min
        if a_before_b:
            # print(direction, a_min, a_max, "before:", b_min)
            return False
        a_after_b  = a_min >= b_max and a_max >= b_max
        if a_after_b:
            # print(direction, a_min, a_max, "after:", b_max)
            return False
        # print(direction, a_before_b, a_after_b)
    # print("bboxes overlap!")
    return True


def get_bbox_intersection(bbox_a, bbox_b):
    """
    calculates intersection bbox of two given bboxes
    :param bboxes:
    :return: BoundingBox: intersecting_bbox
    """
    combined_bbox = BoundingBoxXYZ()
    bboxes = [bbox_a, bbox_b]

    if bboxes_overlap(bbox_a, bbox_b):
        min_xs = set()
        min_ys = set()
        min_zs = set()
        max_xs = set()
        max_ys = set()
        max_zs = set()

        for bbox in bboxes:
            min_xs.add(bbox.Min.X)
            min_ys.add(bbox.Min.Y)
            min_zs.add(bbox.Min.Z)
            max_xs.add(bbox.Max.X)
            max_ys.add(bbox.Max.Y)
            max_zs.add(bbox.Max.Z)

        combined_bbox.Min = XYZ(max(min_xs),
                                max(min_ys),
                                max(min_zs))
        combined_bbox.Max = XYZ(min(max_xs),
                                min(max_ys),
                                min(max_zs))

        return combined_bbox


def bbox_long_edge_is_x_vector(bbox):
    """
    Checks if long edge of bbox is x-vector
    :param bbox:
    :return: Bool
    """
    return bbox.Max.X - bbox.Min.X > bbox.Max.Y - bbox.Min.Y


def bbox_long_edge_is_y_vector(bbox):
    """
    Checks if long edge of bbox is y-vector
    :param bbox:
    :return: Bool
    """
    return bbox.Max.X - bbox.Min.X < bbox.Max.Y - bbox.Min.Y


def bbox_edge_length(bbox, vector):
    """
    Returns the length of a bbox edge of the given vector.
    :param bbox:
    :param vector:
    :return: float
    """
    if vector == "x":
        return (bbox.Max.X - bbox.Min.X)
    elif vector == "y":
        return (bbox.Max.Y - bbox.Min.Y)
    elif vector == "z":
        return (bbox.Max.Z - bbox.Min.Z)


def bbx_min_max_str(bbox):
    """
    Stringify Min and Max of given BoundingBox
    :param bbox: BoundingBox
    :return: str coordinates
    """
    x_min = bbox.Min.X
    y_min = bbox.Min.Y
    z_min = bbox.Min.Z
    x_max = bbox.Max.X
    y_max = bbox.Max.Y
    z_max = bbox.Max.Z
    coord_tuple = (
        x_min, y_min, z_min,
        x_max, y_max, z_max,
    )
    return str(coord_tuple)

