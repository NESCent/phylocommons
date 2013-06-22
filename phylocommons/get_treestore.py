from treestore import Treestore
import settings


def get_treestore():
    return Treestore(**settings.TREESTORE_KWARGS)

def uri_from_tree_id(tree_id):
    return Treestore.uri_from_id(tree_id, base_uri=settings.TREE_URI)

def tree_id_from_uri(uri):
    if uri.startswith(settings.TREE_URI):
        uri = uri.replace(settings.TREE_URI, '', 1)
    if uri.endswith('/'): uri = uri.rstrip('/')
    return uri