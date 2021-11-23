from Login.models import M_User, T_Attr
from Books.models import T_Record

def make_user_config_data(username:str) -> dict:
    """
    username からuser_configページで表示するデータを作る

    Args:
        username (str): M_User.username

    Returns:
        dict: {"name": name, "auth": auth:list, "genre": genre:list} の形の辞書
    """
    user = M_User.objects.get(username = username)
    name = user.name
    auth = list(T_Attr.objects.filter(id=user.username, code=0).order_by("string").values_list('string', flat=True))
    genre = list(T_Attr.objects.filter(id=user.username, code=1).order_by("string").values_list('string', flat=True))
    readdata = list(T_Record.objects.filter(username=user.username, readflag=True).order_by("readdate").values())
    not_readdata = list(T_Record.objects.filter(username=user.username, readflag=False).order_by("readdate").values())
    data ={"name": name, "auth": auth, "genre": genre, "readdata":readdata, "not_readdata": not_readdata}
    return data