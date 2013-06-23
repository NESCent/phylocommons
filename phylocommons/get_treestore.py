from treestore import Treestore
import settings


def get_treestore():
    return Treestore(**settings.TREESTORE_KWARGS)

def uri_from_tree_id(tree_id):
    return Treestore.uri_from_id(tree_id, base_uri=settings.TREE_URI)

def tree_id_from_uri(uri):
    return Treestore.id_from_uri(uri, base_uri=settings.TREE_URI)
