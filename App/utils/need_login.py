from functools import wraps
from django.shortcuts import render

def need_login(redirect_field_name:str, err_msg:str, view_func=None):
    """
    login が必要な場所で使う。
    loginしていない時に、redirecr_field_name に{'msg':err_masg} を付与してrenderする。
    Args:
        redirect_field_name (str): loginしていなかったときに、表示したいページ
        view_func (function, optional): viewe関数.
        err_msg (str, optional): loginしていなかったときに表示したい文字列 Defaults to None.

    Returns:
        [type]: [description]
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return func(request, *args, **kwargs)
            msg={"msg":err_msg}
            return render(request, redirect_field_name, msg)
        return wrapper
    return decorator



      