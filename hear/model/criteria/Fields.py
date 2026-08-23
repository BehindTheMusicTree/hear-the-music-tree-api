from hear.model.uploaded_track_mixin.Fields import Fields as UploadedTrackMixinFields


class Fields(UploadedTrackMixinFields):
    ASCENDANTS = "ascendants"
    ASCENDANTS_RELS = "ascendants_rels"
    DESCENDANTS = "descendants"
    DESCENDANTS_RELS = "descendants_rels"
    ROOT = "root"
    PARENT = "parent"
    CHILD = "child"
    CHILDREN = "children"
    CRITERIA_PLAYLIST = "criteria_playlist"
    TREE = "tree"
