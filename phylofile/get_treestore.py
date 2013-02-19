from treestore import Treestore
import settings


def get_treestore():
    return Treestore()

def tree_id_to_uri(tree_id):
    return (settings.DOMAIN + '/trees/%s' % tree_id)