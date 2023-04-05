from .forms import ChangePasswordForm

def changePasswordForm(request):
    return {'changePasswordForm':ChangePasswordForm}