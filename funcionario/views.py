from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('change_password')  # substitua "nome_da_view" pelo nome da sua view


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Manter a sessão do usuário após mudança de senha
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('/')
        else:
            if 'old_password' in form.errors:
                messages.error(request, 'Sua senha atual está incorreta.')
            if 'new_password1' in form.errors:
                messages.error(request, 'A nova senha não é válida.')
            if 'new_password2' in form.errors:
                messages.error(request, 'As senhas não correspondem.')
            return render(request, 'change_password.html', {'form': form, 'messages': messages.get_messages(request)})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})