from treestore import Treestore
import settings


def get_treestore():
    return Treestore(**settings.TREESTORE_KWARGS)

def uri_from_tree_id(tree_id):
    return (settings.TREE_URI + tree_id)

def tree_id_from_uri(uri):
    if uri.startswith(settings.TREE_URI):
        uri = uri.replace(settings.TREE_URI, '', 1)
    return uri