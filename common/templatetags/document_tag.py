from django import template

register = template.Library()

def is_image(extension):
    extension_list = [
        'bmp',
        'gif',
        'jpg',
        'jpeg',
        'png',
        'psd',
        'tif',
        'tiff',
    ]
    return extension.lower() in extension_list

def is_audio(extension):
    extension_list = ['aif', 'iff', 'm3u', 'm4a', 'mid', 'mp3', 'mpa', 'wav', 'wma']
    return extension.lower() in extension_list

def is_video(extension):
    extension_list = ['avi', 'mp4', 'mpg', 'wmv']
    return extension.lower() in extension_list

def is_pdf(extension):
    extension_list = ['pdf']
    return extension.lower() in extension_list

def is_text(extension):
    extension_list = ['doc','docx', 'log', 'rtf', 'txt']
    return extension.lower() in extension_list

def is_sheet(extension):
    extension_list = ['csv', 'xls', 'xlsx', 'xlsm']
    return extension.lower() in extension_list

def is_archive(extension):
    extension_list = ['zip', '7Z', 'gz', 'rar', 'tar']
    return extension.lower() in extension_list

@register.filter
def sub(value, arg):
    return value - int(arg)

@register.filter
def delete_condition(user, task):
    if user == task.created_by or user.role == "ADMIN":
        return True
    return False

@register.filter
def edit_condition(user, task):
    if (user == task.created_by
        or user.role == "ADMIN"
        or user.has_sales_access
        or user in task.assigned_to.all()
    ):
        return True
    return False