from fastapi import  Form, Request



def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            if arg.annotation not in (Request,)
            else arg
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls
